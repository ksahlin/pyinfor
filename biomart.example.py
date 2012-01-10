# ### R code from vignette source 'vignettes/biomaRt/inst/doc/biomaRt.Rnw'
# 
# ###################################################
# ### code chunk number 1: annotate
# ###################################################
# ## library("annotate")
# options(width=120)
# 
# 
# ###################################################
# ### code chunk number 2: biomaRt
# ###################################################
# library("biomaRt")
# listMarts()
# 
  import biomart
  m = biomart.BioMart()
  m.available_datasets()

# 
# ###################################################
# ### code chunk number 3: ensembl1
# ###################################################
# ensembl=useMart("ensembl")
# 
  m = biomart.BioMart(mart="ensembl")
or
  m = biomart.BioMart()
  m.use_mart("ensembl")

# 
# ###################################################
# ### code chunk number 4: listDatasets
# ###################################################
# listDatasets(ensembl)
# 
  m.available_datasets(mart="ensembl")

# 
# ###################################################
# ### code chunk number 5: ensembl2
# ###################################################
# ensembl = useMart("ensembl",dataset="hsapiens_gene_ensembl")
# 
  ensembl = biomart.BioMart(mart="ensembl", dataset="hsapiens_gene_ensembl")

# 
# ###################################################
# ### code chunk number 6: filters
# ###################################################
# filters = listFilters(ensembl)
# filters[1:5,]
# 
  filters = ensembl.available_filters(dataset="hsapiens_gene_ensembl")
  filters[:5]

# 
# ###################################################
# ### code chunk number 7: attributes
# ###################################################
# attributes = listAttributes(ensembl)
# attributes[1:5,]
# 
  attributes = ensembl.available_attributes(dataset="hsapiens_gene_ensembl")
  attributes[:5]

# 
# ###################################################
# ### code chunk number 8: biomaRt.Rnw:114-116 (eval = FALSE)
# ###################################################
# ## affyids=c("202763_at","209310_s_at","207500_at")
# ## getBM(attributes=c('affy_hg_u133_plus_2', 'entrezgene'), filters = 'affy_hg_u133_plus_2', values = affyids, mart = ensembl)
# 

  affyids=("202763_at","209310_s_at","207500_at")
  attributes=('affy_hg_u133_plus_2', 'entrezgene')
  filters = {'affy_hg_u133_plus_2': affyids}
  
  # ensembl.get_BM(attributes=attributes, filters=filters) is also OK
  ensembl.get_BM(dataset=dataset, attributes=attributes, filters=filters)

# 
# ###################################################
# ### code chunk number 9: biomaRt.Rnw:134-137 (eval = FALSE)
# ###################################################
# ## affyids=c("202763_at","209310_s_at","207500_at")
# ## getBM(attributes=c('affy_hg_u133_plus_2', 'hgnc_symbol', 'chromosome_name','start_position','end_position', 'band'),
# ##  filters = 'affy_hg_u133_plus_2', values = affyids, mart = ensembl)
# 
  affyids=("202763_at","209310_s_at","207500_at")
  # ensembl.get_BM(attributes=('affy_hg_u133_plus_2', 'hgnc_symbol', 'chromosome_name','start_position','end_position', 'band'), filters={'affy_hg_u133_plus_2': affyids}) is also OK
  ensembl.get_BM(attributes=('affy_hg_u133_plus_2', 'hgnc_symbol', 'chromosome_name','start_position','end_position', 'band'), filters={'affy_hg_u133_plus_2': affyids}, dataset="hsapiens_gene_ensembl")

# 
# ###################################################
# ### code chunk number 10: biomaRt.Rnw:152-155 (eval = FALSE)
# ###################################################
# ## entrez=c("673","837")
# ## goids = getBM(attributes=c('entrezgene','go_id'), filters='entrezgene', values=entrez, mart=ensembl)
# ## head(goids)
# 
     entrez = ("673","837")
     # goids = ensembl.get_BM(attributes=('entrezgene','go_id'), filters={'entrezgene': entrez}) is also OK
     goids = ensembl.get_BM(attributes=('entrezgene','go_id'), filters={'entrezgene': entrez}, dataset='hsapiens_gene_ensembl')

# 
# ###################################################
# ### code chunk number 11: biomaRt.Rnw:195-197 (eval = FALSE)
# ###################################################
# ## refseqids = c("NM_005359","NM_000546")
# ## ipro = getBM(attributes=c("refseq_dna","interpro","interpro_description"), filters="refseq_dna",values=refseqids, mart=ensembl)
# 
# 
# ###################################################
# ### code chunk number 12: biomaRt.Rnw:219-221
# ###################################################
# getBM(c('affy_hg_u133_plus_2','ensembl_gene_id'), filters = c('chromosome_name','start','end'),
#  values=list(16,1100000,1250000), mart=ensembl)
# 
# 
# ###################################################
# ### code chunk number 13: biomaRt.Rnw:228-229 (eval = FALSE)
# ###################################################
# ## getBM(c('entrezgene','hgnc_symbol'), filters='go', values='GO:0004707', mart=ensembl)
# 
# 
# ###################################################
# ### code chunk number 14: biomaRt.Rnw:250-252 (eval = FALSE)
# ###################################################
# ## entrez=c("673","7157","837")
# ## getSequence(id = entrez, type="entrezgene",seqType="coding_gene_flank",upstream=100, mart=ensembl) 
# 
# 
# ###################################################
# ### code chunk number 15: biomaRt.Rnw:260-263 (eval = FALSE)
# ###################################################
# ## utr5 = getSequence(chromosome=3, start=185514033, end=185535839,
# ##                       type="entrezgene",seqType="5utr", mart=ensembl)
# ## utr5
# 
# 
# ###################################################
# ### code chunk number 16: biomaRt.Rnw:280-283 (eval = FALSE)
# ###################################################
# ## protein = getSequence(id=c(100, 5728),type="entrezgene",
# ##                         seqType="peptide", mart=ensembl)
# ## protein
# 
# 
# ###################################################
# ### code chunk number 17: biomaRt.Rnw:299-300 (eval = FALSE)
# ###################################################
# ## snpmart = useMart("snp", dataset="hsapiens_snp")
# 
# 
# ###################################################
# ### code chunk number 18: biomaRt.Rnw:307-308 (eval = FALSE)
# ###################################################
# ## getBM(c('refsnp_id','allele','chrom_start','chrom_strand'), filters = c('chr_name','chrom_start','chrom_end'), values = list(8,148350,148612), mart = snpmart)
# 
# 
# ###################################################
# ### code chunk number 19: biomaRt.Rnw:361-362
# ###################################################
# listMarts(archive=TRUE)
# 
# 
# ###################################################
# ### code chunk number 20: biomaRt.Rnw:367-368 (eval = FALSE)
# ###################################################
# ## ensembl = useMart("ensembl_mart_46", dataset="hsapiens_gene_ensembl", archive = TRUE)
# 
# 
# ###################################################
# ### code chunk number 21: biomaRt.Rnw:379-382 (eval = FALSE)
# ###################################################
# ## listMarts(host='may2009.archive.ensembl.org')
# ## ensembl54=useMart(host='may2009.archive.ensembl.org', biomart='ENSEMBL_MART_ENSEMBL')
# ## ensembl54=useMart(host='may2009.archive.ensembl.org', biomart='ENSEMBL_MART_ENSEMBL', dataset='hsapiens_gene_ensembl')
# 
# 
# ###################################################
# ### code chunk number 22: biomaRt.Rnw:391-398 (eval = FALSE)
# ###################################################
# ## wormbase=useMart("wormbase_current",dataset="wormbase_gene")
# ## listFilters(wormbase)
# ## listAttributes(wormbase)
# ## getBM(attributes=c("name","rnai","rnai_phenotype","phenotype_desc"),
# ##                      filters="gene_name", values=c("unc-26","his-33"),
# ##                      mart=wormbase)
# ##      
# 
# 
# ###################################################
# ### code chunk number 23: biomaRt.Rnw:453-454
# ###################################################
# filterType("with_affy_hg_u133_plus_2",ensembl)
# 
# 
# ###################################################
# ### code chunk number 24: biomaRt.Rnw:463-464
# ###################################################
# filterOptions("biotype",ensembl)
# 
# 
# ###################################################
# ### code chunk number 25: biomaRt.Rnw:479-481
# ###################################################
# pages = attributePages(ensembl)
# pages
# 
# 
# ###################################################
# ### code chunk number 26: biomaRt.Rnw:488-489
# ###################################################
# listAttributes(ensembl, page="feature_page")
# 
# 
# ###################################################
# ### code chunk number 27: biomaRt.Rnw:512-514
# ###################################################
# sessionInfo()
# warnings()


