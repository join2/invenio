## This file is part of Invenio.
## Copyright (C) 2012 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import urllib
import cgi

from invenio.config import CFG_SITE_URL, \
     CFG_SITE_LANG, CFG_SITE_RECORD, CFG_INSPIRE_SITE
from invenio.messages import gettext_set_language
from invenio.dateutils import convert_datestruct_to_dategui
from invenio.urlutils import create_html_link

class Template:

    # Parameters allowed in the web interface for fetching files
    files_default_urlargd = {
        'version': (str, ""), # version "" means "latest"
        'docname': (str, ""), # the docname (optional)
        'format' : (str, ""), # the format
        'verbose' : (int, 0), # the verbosity
        'subformat': (str, ""), # the subformat
        'download': (int, 0), # download as attachment
        }

    def tmpl_filelist(self, ln, filelist='', recid='', docname='', version=''):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'recid' *int* - The record id

          - 'docname' *string* - The document name

          - 'version' *int* - The version of the document

          - 'filelist' *string* - The HTML string of the filelist (produced by the BibDoc classes)
        """

        # load the right message language
        _ = gettext_set_language(ln)

        title = _("record") + ' #' + '<a href="%s/%s/%s">%s</a>' % (CFG_SITE_URL, CFG_SITE_RECORD, recid, recid)
        if docname != "":
            title += ' ' + _("document") + ' #' + cgi.escape(str(docname))
        if version != "":
            title += ' ' + _("version") + ' #' + str(version)

        out = """<div style="width:90%%;margin:auto;min-height:100px;margin-top:10px">
                <!--start file list-->
                  %s
                <!--end file list--></div>
              """ % (filelist)

        return out

    def tmpl_bibrecdoc_filelist(self, ln, types, verbose_files=''):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'types' *array* - The different types to display, each record in the format:

               - 'name' *string* - The name of the format

               - 'content' *array of string* - The HTML code produced by tmpl_bibdoc_filelist, for the right files

          - 'verbose_files' - A string representing in a verbose way the
          file information.
        """
        from invenio.config import CFG_BIBDOCFILE_DOCUMENT_FILE_MANAGER_DOCTYPES

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""
        for mytype in types:
            dspname = mytype['name']
            if mytype['name'] in dict(CFG_BIBDOCFILE_DOCUMENT_FILE_MANAGER_DOCTYPES):
                dspname = dict(CFG_BIBDOCFILE_DOCUMENT_FILE_MANAGER_DOCTYPES)[mytype['name']]
            if mytype['name']:
                if not (CFG_INSPIRE_SITE and mytype['name'] == 'INSPIRE-PUBLIC'):
                    out += "<small><b>%s</b> %s:</small>" % (dspname, _("file(s)"))
            out += "<ul>"
            for content in mytype['content']:
                out += content
            out += "</ul>"
            if verbose_files:
                out += "<pre>%s</pre>" % verbose_files
        return out

    def tmpl_bibdoc_filelist(self, ln, versions=None, imageurl='', recid='', docname='', status=''):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'versions' *array* - The different versions to display, each record in the format:

               - 'version' *string* - The version

               - 'content' *string* - The HTML code produced by tmpl_bibdocfile_filelist, for the right file

               - 'previous' *bool* - If the file has previous versions

          - 'imageurl' *string* - The URL to the file image

         - 'recid' *int* - The record id

         - 'docname' *string* - The name of the document

         - 'status' *string* - An non-empty string (ex. 'Restricted') if the file is restricted
                               for the guest user, otherwise an empty string.
        """
        if versions is None:
            versions = []

        # load the right message language
        _ = gettext_set_language(ln)

        out = """<table border="0" cellspacing="1" class="searchbox">
                   %(restriction_label)s
                   <tr>
                     <td align="left" colspan="2" class="portalboxheader">
                       <img src='%(imageurl)s' border="0" />&nbsp;&nbsp;%(docname)s
                     </td>
                   </tr>""" % {
                     'imageurl' : imageurl,
                     'docname' : cgi.escape(docname),
                     'restriction_label': status and ('<tr><td colspan="2" class="restrictedfilerowheader">%s</td></tr>' % _('Restricted')) or ''
                   }
        for version in versions:
            if version['previous']:
                versiontext =  """<br />(%(see)s <a href="%(siteurl)s/%(CFG_SITE_RECORD)s/%(recID)s/files/?docname=%(docname)s&amp;version=all%(ln_link)s">%(previous)s</a>)""" % {
                                 'see' : _("see"),
                                 'siteurl' : CFG_SITE_URL,
                                 'CFG_SITE_RECORD': CFG_SITE_RECORD,
                                 'docname' : cgi.escape(urllib.quote(docname), True),
                                 'recID': recid,
                                 'previous': _("previous"),
                                 'ln_link': (ln != CFG_SITE_LANG and '&amp;ln=' + ln) or '',
                               }
            else:
                versiontext = ""
            out += """<tr>
                        <td class="portalboxheader">
                          <font size="-2">%(version)s %(ver)s%(text)s</font>
                        </td>
                        <td>
                          <table>
                        """ % {
                          'version' : _("version"),
                          'ver' : version['version'],
                          'text' : versiontext,
                        }
            for content in version['content']:
                out += content
            out += "</table></td></tr>"
        out += "</table>"
        return out

    def tmpl_bibdocfile_filelist(self, ln, recid, name, version, md, superformat, subformat, nice_size, description):
        """
        Displays a file in the file list.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'recid' *int* - The id of the record

          - 'name' *string* - The name of the file

          - 'version' *string* - The version

          - 'md' *datetime* - the modification date

          - 'superformat' *string* - The display superformat

          - 'subformat' *string* - The display subformat

          - 'nice_size' *string* - The nice_size of the file

          - 'description' *string* - The description that might have been associated
          to the particular file
        """

        # load the right message language
        _ = gettext_set_language(ln)

        urlbase = '%s/%s/%s/files/%s' % (
            CFG_SITE_URL,
            CFG_SITE_RECORD,
            recid,
            '%s%s' % (cgi.escape(name, True), superformat))

        urlargd = {'version' : version}
        if subformat:
            urlargd['subformat'] = subformat

        link_label = '%s%s' % (name, superformat)
        if subformat:
            link_label += ' (%s)' % subformat

        link = create_html_link(urlbase, urlargd, cgi.escape(link_label))

        return """<tr>
                    <td valign="top">
                      <small>%(link)s</small>
                    </td>
                    <td valign="top">
                      <font size="-2" color="green">[%(nice_size)s]</font>
                      <font size="-2"><em>%(md)s</em>
                    </td>
                    <td valign="top"><em>%(description)s</em></td>
                    </tr>""" % {
                      'link' : link,
                      'nice_size' : nice_size,
                      'md' : convert_datestruct_to_dategui(md.timetuple(), ln),
                      'description' : cgi.escape(description),
                    }

