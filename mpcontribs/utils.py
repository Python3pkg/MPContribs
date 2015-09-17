from __future__ import unicode_literals, print_function
import os, re, pwd, six, time, json
from mpcontribs.io.core.recdict import RecursiveDict
from mpcontribs.io.core.utils import nest_dict, get_short_object_id
from mpcontribs.config import SITE
from mpcontribs.rest.rester import MPContribsRester
from mpcontribs.rest.adapter import ContributionMongoAdapter
from mpcontribs.builders import MPContributionsBuilder
from importlib import import_module

ENDPOINT, API_KEY = "{}/rest".format(SITE), os.environ.get('MAPI_KEY_LOC')

def submit_mpfile(path_or_mpfile, fmt='archieml'):
    with MPContribsRester(API_KEY, endpoint=ENDPOINT) as mpr:
        try:
            yield 'DB connection? ' # also checks internet connection
            ncontribs = sum(1 for contrib in mpr.query_contributions())
            yield 'OK ({} contributions).</br> '.format(ncontribs)
            time.sleep(1)
            yield 'Contributor? '
            check = mpr.check_contributor()
            yield '{} ({}).</br>'.format(check['contributor'], check['institution'])
            time.sleep(1)
            yield 'Registered? '
            if not check['is_contrib']:
                raise Exception('Please register as contributor!')
            time.sleep(1)
            yield 'YES.</br>'
            time.sleep(1)
            yield 'Cancel data transmission? '
            for i in range(5):
                yield '#'
                time.sleep(1)
            yield ' NO.</br>'
            # call process_mpfile with target=mpr
        except Exception as ex:
            yield 'FAILED.</br>'
            yield str(ex)
            return

def process_mpfile(path_or_mpfile, target=None, fmt='archieml'):
    if isinstance(path_or_mpfile, six.string_types) and \
       not os.path.isfile(path_or_mpfile):
        yield '{} not found'.format(path_or_mpfile)
        return
    mod = import_module('mpcontribs.io.{}.mpfile'.format(fmt))
    MPFile = getattr(mod, 'MPFile')
    if target is None:
        from mpcontribs.rest.adapter import ContributionMongoAdapter
        from mpcontribs.builders import MPContributionsBuilder
        full_name = pwd.getpwuid(os.getuid())[4]
        contributor = '{} <phuck@lbl.gov>'.format(full_name)
        cma = ContributionMongoAdapter()
    # split input MPFile into contributions: treat every mp_cat_id as separate DB insert
    mpfile, cid_shorts = MPFile.from_dict(), [] # output
    for idx, mpfile_single in enumerate(MPFile.from_file(path_or_mpfile).split()):
        mp_cat_id = mpfile_single.document.keys()[0]
        cid = mpfile_single.document[mp_cat_id].get('cid', None)
        update = bool(cid is not None)
        if update:
            cid_short = get_short_object_id(cid)
            yield 'use contribution #{} to update ID #{} ... '.format(idx, cid_short)
        else:
            yield 'submit contribution #{} ... '.format(idx, mp_cat_id)
        if target is not None:
            cid = target.submit_contribution(mpfile_single)
        else:
            doc = cma.submit_contribution(mpfile_single, contributor)
            cid = doc['_id']
        cid_short = get_short_object_id(cid)
        yield 'done.</br>' if update else 'done (ID #{}).</br>'.format(cid_short)
        mpfile_single.insert_id(mp_cat_id, cid)
        cid_shorts.append(cid_short)
        yield 'build contribution #{} into {} ... '.format(idx, mp_cat_id)
        if target is not None:
            url = target.build_contribution(cid)
            yield 'done, see {}/{}.</br>'.format(SITE, url)
        else:
            mcb = MPContributionsBuilder(doc)
            yield mcb.build(contributor, cid)
            yield 'done.</br>'.format(idx, cid_short)
        mpfile.concat(mpfile_single)
    ncontribs = len(cid_shorts)
    if target is not None and \
       isinstance(path_or_mpfile, six.string_types) and \
       os.path.isfile(path_or_mpfile):
        yield 'embed #{} in MPFile ...'.format('/'.join(cid_shorts))
        mpfile.write_file(path_or_mpfile, with_comments=True)
        yield '<strong>{} contributions successfully submitted.</strong>'.format(ncontribs)
    else:
        yield '<strong>{} contributions successfully processed.</strong>'.format(ncontribs)
