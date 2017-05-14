Setup Solr with Memopol
=======================

Solr is used to perform search in the data. Currently, it is used only for
reprensatative search autocomplete.

This howto will be based on the current stable version of Debian (jessie).

Installation on Debian Stable
-----------------------------

Solr is in the official repository of debian, you can install it launching::

    # apt install solr-tomcat/stable
    Package: solr-tomcat
    Source: lucene-solr
    Version: 3.6.2+dfsg-5
    Installed-Size: 65,5 kB
    Maintainer: Debian Java Maintainers <pkg-java-maintainers@lists.alioth.debian.org>
    Depends: solr-common (= 3.6.2+dfsg-5), tomcat7
    Conflicts: solr-jetty, solr-tomcat6
    Homepage: http://lucene.apache.org
    Section: java
    Priority: optional
    Download-Size: 8 598 B
    APT-Sources: http://ftp.fr.debian.org/debian/ jessie/main amd64 Packages
    Description: Enterprise search server based on Lucene3 - Tomcat integration
     Solr is an open source enterprise search server based on the Lucene
     Java search library, with XML/HTTP and JSON APIs, hit highlighting,
     faceted search, caching, replication, and a web administration
     interface. It runs in a Java servlet container such as Tomcat.
     .
     This package provides the Tomcat integration files for Solr.


By default, the solr server is listen on localhost:8080. Memopol is configured
to use this addess by default, in production. If you install a newer version of
Solr (6.5.1 is the latest release), you should update the settings.py::

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8080/solr',
        },
    }

Configure Solr
---------------

You can use the default Solr configuration to use it, You just need to generate
the schema.xml file and copy it in `/etc/solr/`. To generate the schema.xml
file::

    $ memopol build_solr_schema > schmema.xml

    ## Copy the schema.xml file into /etc/solr/conf
    $ sudo cp schema.xml /etc/solr/conf/

    ## Restart tomcat
    $ sudo /etc/init.d/tomcat7 restart

Last step, you need to build the index by using::

    $ memopol rebuild_index

The solr is now setup and production ready.

Populate data in Solr
---------------------

Django-haystack plugin offers two ways to populate data. The first way is by
using a cron job to update the index, the other way is to use `Dango signals to
update / delete datas <https://django-haystack.readthedocs.io/en/v2.6.0/signal_processors.html>`_.

For now, Haystack is not configured to be used with Django signals. It is 
necessary to add a cron job to update the index ::

    $ memopol update_index

`More informations about cron with Solr <http://django-haystack.readthedocs.io/en/v2.6.0/searchindex_api.html?highlight=cron#keeping-the-index-fresh>`_
