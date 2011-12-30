import httplib, time, urllib, urllib2, re, webbrowser
import sys

"""
to interact with martservice through www.biomart.org

Author: Xiao Jianfeng
last updated: 2011.11.5

http://www.biomart.org/martservice.html
	
 BioMart  	 MartService

(a) Querying BioMart

To submit a query using our webservices generate an XML document conforming to our Query XML syntax. This can be achieved simply by building up your query using MartView and hitting the XML button. This XML should be posted to http://www.biomart.org/martservice attached to a single parameter of query. For example you could either:

    save your query as Query.xml and then POST this using the webExample.pl script in our biomart-perl/scripts installation.
    submit using wget: wget -O results.txt 'http://www.biomart.org/biomart/martservice?query=MY_XML' replacing MY_XML with the XML obtained above, first removing any new lines.


(b) Retrieving Meta Data

    to retrieve registry information: http://www.biomart.org/biomart/martservice?type=registry
    to retrieve datasets available for a mart: http://www.biomart.org/biomart/martservice?type=datasets&mart=ensembl
    to retrieve attributes available for a dataset: http://www.biomart.org/biomart/martservice?type=attributes&dataset=oanatinus_gene_ensembl
    to retrieve filters available for a dataset: http://www.biomart.org/biomart/martservice?type=filters&dataset=oanatinus_gene_ensembl
    to retrieve configuration for a dataset: http://www.biomart.org/biomart/martservice?type=configuration&dataset=oanatinus_gene_ensembl


  	SOAP Access
The SOAP based access is functionally equivalent to the REST style access described above. For description on BioMart SOAP based Web Service (MartServiceSoap), see:

    MartServiceSoap Endpoint (for SOAP based access only): http://www.biomart.org/biomart/martsoap
    MartServiceSoap WSDL: http://www.biomart.org/biomart/martwsdl
    MartServiceSoap XSD: http://www.biomart.org/biomart/martxsd


For more information see the web services section of our documentation.
Page last updated: 05/10/2011 15:25:40

http://www.biomart.org/faqs.html is also worth reading. Many examples how to build queries are available here!!
"""

example1 = """
output: --------------------------------------------------------------------------------------------
HGNC symbol 	Affy HC G110 	Ensembl Gene ID 	EntrezGene ID 	Ensembl Transcript ID
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000371884
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000294339
TAL1 		ENSG00000162367 	6886 	ENST00000459729
TAL1 		ENSG00000162367 	6886 	ENST00000464796
TAL1 		ENSG00000162367 	6886 	ENST00000481091
TAL1 		ENSG00000162367 	6886 	ENST00000465912
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000371883
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000310638
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000475477
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000462347

query:  --------------------------------------------------------------------------------------------     
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE Query>
    <Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
                            
            <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
                    <Filter name = "ensembl_gene_id" value = "ENSG00000162367,ENSG00000187048"/>
                    <Attribute name = "hgnc_symbol" />
                    <Attribute name = "affy_hc_g110" />
                    <Attribute name = "ensembl_gene_id" />
                    <Attribute name = "entrezgene" />
                    <Attribute name = "ensembl_transcript_id" />
            </Dataset>
    </Query>

left side of biomart:  -------------------------------------------------------------------------------
    Dataset
    Homo sapiens genes (GRCh37.p5)
    Filters
    Ensembl Gene ID(s) [e.g. ENSG00000139618]: [ID-list specified]
    Attributes
    HGNC symbol
    Affy HC G110
    Ensembl Gene ID
    EntrezGene ID
    Ensembl Transcript ID
    """
DEBUG = False

mart_host = "www.biomart.org"
mart_url_prefix = "/biomart/martservice?"

#Note: if header = "0" --> no header; header = "1" or "ture" --> with header
# limit = N could also be added 
mart_query_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "1" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >

"""
mart_query_database = None
mart_query_dataset = None
mart_query_filters = None
mart_query_attributes = ["ensembl_gene_id", "ensembl_transcript_id",] # default value

def reporthook(blocks_read, block_size, total_size):
    """
    could be used to report progress while downloading.

    url = 'http://www.biomart.org/biomart/martservice?'
    query4 = '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "1" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >

        <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
                <Attribute name = "ensembl_gene_id" />
                <Attribute name = "ensembl_transcript_id" />
                <Attribute name = "external_gene_id" />
                <Attribute name = "external_transcript_id" />
                <Attribute name = "hgnc_id" />
                <Attribute name = "hgnc_transcript_name" />
                <Attribute name = "hgnc_symbol" />
        </Dataset>
</Query>
'
    b = urllib.urlretrieve(url=url, data=urllib.urlencode(dict(query=query4)), reporthook=biomart.reporthook)

    But it would be difficult to set timeout for this method.
    """

    if DEBUG:
        print >> sys.stderr, blocks_read, block_size, total_size,
    if not blocks_read:
     print >> sys.stderr, 'Opened',
     return
    if total_size < 0:
     # Unknown size
     print >> sys.stderr, '\rRead %d blocks' % blocks_read,
    else:
     amount_read = blocks_read * block_size
     print >> sys.stderr, '\rRead %d blocks, or %d/%d' % (blocks_read, amount_read, total_size),
    return

class BioMart:

    def __init__(self):
        self.con = httplib.HTTPConnection(mart_host, timeout=1000)
        self.mart_query_database = None
        self.mart_query_dataset = None
        self.mart_query_filters = None
        self.mart_query_attributes = None

    def test(self):

        mart_query_example = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
                        
        <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
                <Filter name = "ensembl_gene_id" value = "ENSG00000162367,ENSG00000187048"/>
                <Attribute name = "hgnc_symbol" />
                <Attribute name = "affy_hc_g110" />
                <Attribute name = "ensembl_gene_id" />
                <Attribute name = "entrezgene" />
                <Attribute name = "ensembl_transcript_id" />
        </Dataset>
</Query>"""
        mart_example_output = """ HGNC symbol 	Affy HC G110 	Ensembl Gene ID 	EntrezGene ID 	Ensembl Transcript ID
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000371884
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000294339
TAL1 		ENSG00000162367 	6886 	ENST00000459729
TAL1 		ENSG00000162367 	6886 	ENST00000464796
TAL1 		ENSG00000162367 	6886 	ENST00000481091
TAL1 		ENSG00000162367 	6886 	ENST00000465912
TAL1 	560_s_at 	ENSG00000162367 	6886 	ENST00000371883
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000310638
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000475477
CYP4A11 	1391_s_at 	ENSG00000187048 	1579 	ENST00000462347
"""
        params = urllib.urlencode({"query": mart_query_example})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def build_query(self):
        mart_query_database = 'ensembl'
        # could be one dataset or more, how to explain multiple datasets remains to be determined
        mart_query_dataset = 'hsapiens_gene_ensembl'
        mart_query_filters = {"chromosome_name": "Y"}
        mart_query_attributes = ["ensembl_gene_id", "ensembl_transcript_id", 
                                 "external_gene_id", "external_transcript_id",
                                 "hgnc_id", "hgnc_transcript_name", "hgnc_symbol"]

        query_str_dataset = """\t<Dataset name = "%s" interface = "default" >\n""" % mart_query_dataset
        query_str_filter = "".join("""\t\t<Filter name = "%s" value = "%s"/>\n""" % (k, v) for k,v in mart_query_filters.items())
        query_str_attributes = "".join("""\t\t<Attribute name = "%s" />\n""" % s for s in mart_query_attributes)

        return mart_query_header + query_str_dataset + query_str_filter + query_str_attributes + "\t</Dataset>\n</Query>"

    def test_query(self):
        query = self.build_query()
        print query

        return self.easy_response(query=query)

    def registry_information(self):
        params = urllib.urlencode({"type":"registry"})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def available_datasets(self):
        """
TableSet	oanatinus_gene_ensembl	Ornithorhynchus anatinus genes (OANA5)	1	OANA5	200	50000	default	2011-09-07 22:26:09
TableSet	tguttata_gene_ensembl	Taeniopygia guttata genes (taeGut3.2.4)	1	taeGut3.2.4	200	50000	default	2011-09-07 22:26:36
TableSet	cporcellus_gene_ensembl	Cavia porcellus genes (cavPor3)	1	cavPor3	200	50000	default	2011-09-07 22:27:40
TableSet	gaculeatus_gene_ensembl	Gasterosteus aculeatus genes (BROADS1)	1	BROADS1	200	50000	default	2011-09-07 22:10:34
TableSet	lafricana_gene_ensembl	Loxodonta africana genes (loxAfr3)	1	loxAfr3	200	50000	default	2011-09-07 22:26:48
TableSet	mlucifugus_gene_ensembl	Myotis lucifugus genes (myoLuc2)	1	myoLuc2	200	50000	default	2011-09-07 22:27:08
TableSet	hsapiens_gene_ensembl	Homo sapiens genes (GRCh37.p5)	1	GRCh37.p5	200	50000	default	2011-09-07 22:10:13
TableSet	choffmanni_gene_ensembl	Choloepus hoffmanni genes (choHof1)	1	choHof1	200	50000	default	2011-09-07 22:17:55
TableSet	csavignyi_gene_ensembl	Ciona savignyi genes (CSAV2.0)	1	CSAV2.0	200	50000	default	2011-09-07 22:10:23
(......)
"""
        params = urllib.urlencode({"type":"datasets", "mart":"ensembl"})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def available_attributes(self, dataset="hsapiens_gene_ensembl"):
        """
        To retrieve available attributes for a given dataset.

        dataset is a valid dataset, for example: hsapiens_gene_ensembl, oanatinus_gene_ensembl, tguttata_gene_ensembl
        dataset could be retrived by self.available_datasets()
        """

        params = urllib.urlencode({"type":"attributes", "dataset":dataset})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def available_filters(self, dataset="hsapiens_gene_ensembl"):
        """
        To retrieve available filters for a given dataset.
        """

        params = urllib.urlencode({"type":"filters", "dataset":dataset})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def configuration(self, dataset="hsapiens_gene_ensembl"):
        """
        To get configuration for a dataset.
        """

        params = urllib.urlencode({"type":"configuration", "dataset":dataset})
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

    def easy_response(self, **params_dict):
        params = urllib.urlencode(params_dict)
        self.con.request(method="POST", url=mart_url_prefix, body=params)
        response = self.con.getresponse()
        print "submit:", response.status, response.reason
        return response.status, response.reason, response.read()

#-----------------------------------------------------------------------
# main
#-----------------------------------------------------------------------
if __name__ == '__main__':
    print BioMart().test()
    raw_input("look")
