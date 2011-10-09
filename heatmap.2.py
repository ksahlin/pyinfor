"""
a direct translation of R gplots heatmap.2
"""

def heatmap(x,
    ## dendrogram control
    Rowv=TRUE,
    Colv=True,           # if(symm)"Rowv" else TRUE,
    distfun=dist,        # find counterpart function in scipy
    hclustfun=hclust,    # find counterpart function in scipy
    dendrogram="both",   # c("both","row","column","none"),
    symm=FALSE,

    ## data scaling
    scale=None,          # c("none","row", "column"),
    na.rm=TRUE,

    ## image plot
    revC=True,           # identical(Colv, "Rowv"),
    add.expr,

    ## mapping data to colors
    breaks,
    symbreaks=None,      # min(x < 0, na.rm=TRUE) || scale!="none",

    ## colors
    col="heat.colors",

    ## block sepration
    colsep,
    rowsep,
    sepcolor="white",
    sepwidth=(0.05, 0.05), # c(0.05,0.05),

    ## cell labeling
    cellnote,
    notecex=1.0,
    notecol="cyan",
    na.color=par("bg"),    # find counterpart function in scipy/matplotlib

    ## level trace
    trace=None,            # c("column","row","both","none"),
    tracecol="cyan",
    hline=median(breaks),  # find counterpart function in scipy/matplotlib
    vline=median(breaks),  # find counterpart function in scipy/matplotlib
    linecol=tracecol,      # need some work

    ## Row/Column Labeling
    margins=(5,5),         # c(5, 5),
    ColSideColors,
    RowSideColors,
    cexRow = 0.2 + 1/log10(nr),  # need some work
    cexCol = 0.2 + 1/log10(nc),  # need some work
    labRow=None,                 # NULL
    labCol=None,                 # NULL

    ## color key + density info
    key=True,                    # TRUE,
    keysize=1.5,
    density.info=c("histogram","density","none"),  # need some work
    denscol=tracecol,                              # need some work
    symkey=min(x < 0, na.rm=TRUE) || symbreaks,    # need some work
    densadj=0.25,

    ## plot labels
    main=None,                                     # NULL,
    xlab=None,                                     # NULL,
    ylab=None,                                     # NULL,

    ## plot layout
    lmat=None,                                     # NULL,
    lhei=None,                                     # NULL,
    lwid=None,                                     # NULL,
    ):
        raise Exception("method not implemented")



#### - - - - - - - original R file - - - - - - - - - ####

## $Id: heatmap.2.R 1463 2010-12-13 16:44:17Z warnes $

heatmap.2 <- function (x,

                       ## dendrogram control
                       Rowv = TRUE,
                       Colv=if(symm)"Rowv" else TRUE,
                       distfun = dist,
                       hclustfun = hclust,
                       dendrogram = c("both","row","column","none"),
                       symm = FALSE,

                       ## data scaling
                       scale = c("none","row", "column"),
                       na.rm=TRUE,

                       ## image plot
                       revC = identical(Colv, "Rowv"),
                       add.expr,

                       ## mapping data to colors
                       breaks,
                       symbreaks=min(x < 0, na.rm=TRUE) || scale!="none",

                       ## colors
                       col="heat.colors",

                       ## block sepration
                       colsep,
                       rowsep,
                       sepcolor="white",
                       sepwidth=c(0.05,0.05),

                       ## cell labeling
                       cellnote,
                       notecex=1.0,
                       notecol="cyan",
                       na.color=par("bg"),

                       ## level trace
                       trace=c("column","row","both","none"),
                       tracecol="cyan",
                       hline=median(breaks),
                       vline=median(breaks),
                       linecol=tracecol,

                       ## Row/Column Labeling
                       margins = c(5, 5),
                       ColSideColors,
                       RowSideColors,
                       cexRow = 0.2 + 1/log10(nr),
                       cexCol = 0.2 + 1/log10(nc),
                       labRow = NULL,
                       labCol = NULL,

                       ## color key + density info
                       key = TRUE,
                       keysize = 1.5,
                       density.info=c("histogram","density","none"),
                       denscol=tracecol,
                       symkey = min(x < 0, na.rm=TRUE) || symbreaks,
                       densadj = 0.25,

                       ## plot labels
                       main = NULL,
                       xlab = NULL,
                       ylab = NULL,

                       ## plot layout
                       lmat = NULL,
                       lhei = NULL,
                       lwid = NULL,

                       ## extras
                       ...
                       )
{
  scale01 <- function(x, low=min(x), high=max(x) )
    {
      x <- (x-low)/(high - low)
      x
    }
  
  retval <- list()
  
  scale <- if(symm && missing(scale)) "none" else match.arg(scale)
  dendrogram <- match.arg(dendrogram)
  trace <- match.arg(trace)
  density.info <- match.arg(density.info)

  if(length(col)==1 && is.character(col) )
    col <- get(col, mode="function")

  if(!missing(breaks) && (scale!="none"))
    warning("Using scale=\"row\" or scale=\"column\" when breaks are",
            "specified can produce unpredictable results.",
            "Please consider using only one or the other.")

  ## key & density don't make sense when data is not all on the same scale
  ##    if(scale!="none" &&  key==TRUE)
  ##      {
  ##        warning("Key cannot be plotted when scale!=\"none\".")
  ##        key=FALSE
  ##      }

  if ( is.null(Rowv) || is.na(Rowv) )
    Rowv <- FALSE
  if ( is.null(Colv) || is.na(Colv) )
    Colv <- FALSE
  else if( Colv=="Rowv" && !isTRUE(Rowv) )
    Colv <- FALSE
  
  
  if(length(di <- dim(x)) != 2 || !is.numeric(x))
    stop("`x' must be a numeric matrix")

  nr <- di[1]
  nc <- di[2]

  if(nr <= 1 || nc <= 1)
    stop("`x' must have at least 2 rows and 2 columns")

  if(!is.numeric(margins) || length(margins) != 2)
    stop("`margins' must be a numeric vector of length 2")

  if(missing(cellnote))
    cellnote <- matrix("", ncol=ncol(x), nrow=nrow(x))

  if(!inherits(Rowv, "dendrogram")) {
    ## Check if Rowv and dendrogram arguments are consistent
    if ( ( (!isTRUE(Rowv)) || (is.null(Rowv))) &&
         (dendrogram %in% c("both","row") ) )
      {
        if (is.logical(Colv) && (Colv))
          dendrogram <- "column"
        else
          dedrogram <- "none"
        
        warning("Discrepancy: Rowv is FALSE, while dendrogram is `",
                dendrogram, "'. Omitting row dendogram.")
        
      }
  }

  if(!inherits(Colv, "dendrogram")) {
    ## Check if Colv and dendrogram arguments are consistent
    if ( ( (!isTRUE(Colv)) || (is.null(Colv)))
        && (dendrogram %in% c("both","column")) )
      {
        if (is.logical(Rowv) && (Rowv))
          dendrogram <- "row"
        else
          dendrogram <- "none"
        
        warning("Discrepancy: Colv is FALSE, while dendrogram is `",
                dendrogram, "'. Omitting column dendogram.")
      }
  }
  
  
  ## by default order by row/col mean
  ## if(is.null(Rowv)) Rowv <- rowMeans(x, na.rm = na.rm)
  ## if(is.null(Colv)) Colv <- colMeans(x, na.rm = na.rm)

  ## get the dendrograms and reordering indices

  ## if( dendrogram %in% c("both","row") )
  ##  { ## dendrogram option is used *only* for display purposes
  if(inherits(Rowv, "dendrogram"))
    {
      ddr <- Rowv ## use Rowv 'as-is', when it is dendrogram
      rowInd <- order.dendrogram(ddr)      
    }
  else if (is.integer(Rowv))
    { ## Compute dendrogram and do reordering based on given vector
      hcr <- hclustfun(distfun(x))
      ddr <- as.dendrogram(hcr)
      ddr <-  reorder(ddr, Rowv)
      
      rowInd <- order.dendrogram(ddr)
      if(nr != length(rowInd))
        stop("row dendrogram ordering gave index of wrong length")
    }
  else if (isTRUE(Rowv)) 
    { ## If TRUE, compute dendrogram and do reordering based on rowMeans
      Rowv <- rowMeans(x, na.rm = na.rm)
      hcr <- hclustfun(distfun(x))
      ddr <- as.dendrogram(hcr)
      ddr <- reorder(ddr, Rowv)
      
      rowInd <- order.dendrogram(ddr)
      if(nr != length(rowInd))
        stop("row dendrogram ordering gave index of wrong length")
    } else {
      rowInd <- nr:1
    }
  
  ## if( dendrogram %in% c("both","column") )
  ##   {
  if(inherits(Colv, "dendrogram"))
    {
      ddc <- Colv ## use Colv 'as-is', when it is dendrogram
      colInd <- order.dendrogram(ddc)
    }
  else if(identical(Colv, "Rowv")) {
    if(nr != nc)
      stop('Colv = "Rowv" but nrow(x) != ncol(x)')
    if(exists("ddr"))
      {
        ddc <- ddr
        colInd <- order.dendrogram(ddc)
      } else
    colInd <- rowInd
  } else if(is.integer(Colv))
    {## Compute dendrogram and do reordering based on given vector
      hcc <- hclustfun(distfun(if(symm)x else t(x)))
      ddc <- as.dendrogram(hcc)
      ddc <- reorder(ddc, Colv)

      colInd <- order.dendrogram(ddc)
      if(nc != length(colInd))
        stop("column dendrogram ordering gave index of wrong length")
    }
  else if (isTRUE(Colv))
    {## If TRUE, compute dendrogram and do reordering based on rowMeans
      Colv <- colMeans(x, na.rm = na.rm)
      hcc <- hclustfun(distfun(if(symm)x else t(x)))
      ddc <- as.dendrogram(hcc)
      ddc <- reorder(ddc, Colv)

      colInd <- order.dendrogram(ddc)
      if(nc != length(colInd))
        stop("column dendrogram ordering gave index of wrong length")
    }
  else
    {
      colInd <- 1:nc
    }

  retval$rowInd <- rowInd
  retval$colInd <- colInd
  retval$call <- match.call()

  
  ## reorder x & cellnote
  x <- x[rowInd, colInd]
  x.unscaled <- x
  cellnote <- cellnote[rowInd, colInd]

  if(is.null(labRow))
    labRow <- if(is.null(rownames(x))) (1:nr)[rowInd] else rownames(x)
  else
    labRow <- labRow[rowInd]

  if(is.null(labCol))
    labCol <- if(is.null(colnames(x))) (1:nc)[colInd] else colnames(x)
  else
    labCol <- labCol[colInd]

  if(scale == "row") {
    retval$rowMeans <- rm <- rowMeans(x, na.rm = na.rm)
    x <- sweep(x, 1, rm)
    retval$rowSDs <-  sx <- apply(x, 1, sd, na.rm = na.rm)
    x <- sweep(x, 1, sx, "/")
  }
  else if(scale == "column") {
    retval$colMeans <- rm <- colMeans(x, na.rm = na.rm)
    x <- sweep(x, 2, rm)
    retval$colSDs <-  sx <- apply(x, 2, sd, na.rm = na.rm)
    x <- sweep(x, 2, sx, "/")
  }

  ## Set up breaks and force values outside the range into the endmost bins
  if(missing(breaks) || is.null(breaks) || length(breaks)<1 )
    {
      if( missing(col) ||  is.function(col) )
        breaks <- 16
      else 
        breaks <- length(col)+1
    }
  
  if(length(breaks)==1)
    {
      if(!symbreaks)
        breaks <- seq( min(x, na.rm=na.rm), max(x,na.rm=na.rm), length=breaks)
      else
        {
          extreme <- max(abs(x), na.rm=TRUE)
          breaks <- seq( -extreme, extreme, length=breaks )
        }
    }

  nbr <- length(breaks)
  ncol <- length(breaks)-1

  if(class(col)=="function")
    col <- col(ncol)

  min.breaks <- min(breaks)
  max.breaks <- max(breaks)

  x[x<min.breaks] <- min.breaks
  x[x>max.breaks] <- max.breaks

  
  ## Calculate the plot layout
  if( missing(lhei) || is.null(lhei) )
    lhei <- c(keysize, 4)

  if( missing(lwid) || is.null(lwid) )
    lwid <- c(keysize, 4)

  if( missing(lmat) || is.null(lmat) )
    {
      lmat <- rbind(4:3, 2:1)
      
      if(!missing(ColSideColors)) { ## add middle row to layout
        if(!is.character(ColSideColors) || length(ColSideColors) != nc)
          stop("'ColSideColors' must be a character vector of length ncol(x)")
        lmat <- rbind(lmat[1,]+1, c(NA,1), lmat[2,]+1)
        lhei <- c(lhei[1], 0.2, lhei[2])
      }

      if(!missing(RowSideColors)) { ## add middle column to layout
        if(!is.character(RowSideColors) || length(RowSideColors) != nr)
          stop("'RowSideColors' must be a character vector of length nrow(x)")
        lmat <- cbind(lmat[,1]+1, c(rep(NA, nrow(lmat)-1), 1), lmat[,2]+1)
        lwid <- c(lwid[1], 0.2, lwid[2])
      }

      lmat[is.na(lmat)] <- 0
    }
  
  if(length(lhei) != nrow(lmat))
    stop("lhei must have length = nrow(lmat) = ", nrow(lmat))

  if(length(lwid) != ncol(lmat))
    stop("lwid must have length = ncol(lmat) =", ncol(lmat))

  ## Graphics `output' -----------------------

  op <- par(no.readonly = TRUE)
  on.exit(par(op))
  layout(lmat, widths = lwid, heights = lhei, respect = FALSE)

  ## draw the side bars
  if(!missing(RowSideColors)) {
    par(mar = c(margins[1],0, 0,0.5))
    image(rbind(1:nr), col = RowSideColors[rowInd], axes = FALSE)
  }
  if(!missing(ColSideColors)) {
    par(mar = c(0.5,0, 0,margins[2]))
    image(cbind(1:nc), col = ColSideColors[colInd], axes = FALSE)
  }
  ## draw the main carpet
  par(mar = c(margins[1], 0, 0, margins[2]))
  #if(scale != "none" || !symm)
  #  {
      x <- t(x)
      cellnote <- t(cellnote)
  #  }
  if(revC)
    { ## x columns reversed
      iy <- nr:1
      if(exists("ddr"))
        ddr <- rev(ddr)
      x <- x[,iy]
      cellnote <- cellnote[,iy]
    }
  else iy <- 1:nr

  ## display the main carpet
  image(1:nc, 1:nr, x, xlim = 0.5+ c(0, nc), ylim = 0.5+ c(0, nr),
        axes = FALSE, xlab = "", ylab = "", col=col, breaks=breaks,
        ...)
  retval$carpet <- x
  if(exists("ddr"))
    retval$rowDendrogram <- ddr
  if(exists("ddc"))
    retval$colDendrogram <- ddc
  retval$breaks <- breaks
  retval$col <- col
  
  ## fill 'na' positions with na.color
  if(!invalid(na.color) & any(is.na(x)))
    {
      mmat <- ifelse(is.na(x), 1, NA)
      image(1:nc, 1:nr, mmat, axes = FALSE, xlab = "", ylab = "",
            col=na.color, add=TRUE)
    }

  ## add labels
  axis(1, 1:nc, labels= labCol, las= 2, line= -0.5, tick= 0, cex.axis= cexCol)
  if(!is.null(xlab)) mtext(xlab, side = 1, line = margins[1] - 1.25)
  axis(4, iy, labels= labRow, las= 2, line= -0.5, tick= 0, cex.axis= cexRow)
  if(!is.null(ylab)) mtext(ylab, side = 4, line = margins[2] - 1.25)

  ## perform user-specified function
  if (!missing(add.expr))
    eval(substitute(add.expr))

  ## add 'background' colored spaces to visually separate sections
  if(!missing(colsep))
    for(csep in colsep)
      rect(xleft =csep+0.5,               ybottom=rep(0,length(csep)),
           xright=csep+0.5+sepwidth[1],     ytop=rep(ncol(x)+1,csep),
           lty=1, lwd=1, col=sepcolor, border=sepcolor)

  if(!missing(rowsep))
    for(rsep in rowsep)
      rect(xleft =0,          ybottom= (ncol(x)+1-rsep)-0.5,
           xright=nrow(x)+1,  ytop   = (ncol(x)+1-rsep)-0.5 - sepwidth[2],
           lty=1, lwd=1, col=sepcolor, border=sepcolor)

  
  ## show traces
  min.scale <- min(breaks)
  max.scale <- max(breaks)
  x.scaled  <- scale01(t(x), min.scale, max.scale)

  if(trace %in% c("both","column") )
    {
      retval$vline <- vline
      vline.vals <- scale01(vline, min.scale, max.scale)
      for( i in colInd )
        {
          if(!is.null(vline))
            {
              abline(v=i-0.5 + vline.vals, col=linecol, lty=2)
            }
          xv <- rep(i, nrow(x.scaled)) + x.scaled[,i] - 0.5
          xv <- c(xv[1], xv)
          yv <- 1:length(xv)-0.5
          lines(x=xv, y=yv, lwd=1, col=tracecol, type="s")
        }
    }

  
  if(trace %in% c("both","row") )
    {
      retval$hline <- hline
      hline.vals <- scale01(hline, min.scale, max.scale)
      for( i in rowInd )
        {
          if(!is.null(hline))
            {
              abline(h=i + hline, col=linecol, lty=2)
            }
          yv <- rep(i, ncol(x.scaled)) + x.scaled[i,] - 0.5
          yv <- rev(c(yv[1], yv))
          xv <- length(yv):1-0.5
          lines(x=xv, y=yv, lwd=1, col=tracecol, type="s")
        }
    }



  if(!missing(cellnote))
    text(x=c(row(cellnote)),
         y=c(col(cellnote)),
         labels=c(cellnote),
         col=notecol,
         cex=notecex)

  ## the two dendrograms :
  par(mar = c(margins[1], 0, 0, 0))
  if( dendrogram %in% c("both","row") )
    {
      plot(ddr, horiz = TRUE, axes = FALSE, yaxs = "i", leaflab = "none")
    }
  else
    plot.new()

  par(mar = c(0, 0, if(!is.null(main)) 5 else 0, margins[2]))

  if( dendrogram %in% c("both","column") )
    {
      plot(ddc, axes = FALSE, xaxs = "i", leaflab = "none")
    }
  else
    plot.new()

  ## title
  if(!is.null(main)) title(main, cex.main = 1.5*op[["cex.main"]])

  ## Add the color-key
  if(key)
    {
      par(mar = c(5, 4, 2, 1), cex=0.75)
      tmpbreaks <- breaks

      if(symkey)
        {
          max.raw <- max(abs(c(x,breaks)),na.rm=TRUE)
          min.raw <- -max.raw
          tmpbreaks[1] <- -max(abs(x), na.rm=TRUE)
          tmpbreaks[length(tmpbreaks)] <- max(abs(x), na.rm=TRUE)
        }
      else
        {
          min.raw <- min(x, na.rm=TRUE) ## Again, modified to use scaled 
          max.raw <- max(x, na.rm=TRUE) ## or unscaled (SD 12/2/03)
        }

      z <- seq(min.raw, max.raw, length=length(col))
      image(z=matrix(z, ncol=1),
            col=col, breaks=tmpbreaks,
            xaxt="n", yaxt="n")

      par(usr=c(0,1,0,1))
      lv <- pretty(breaks)
      xv <- scale01(as.numeric(lv), min.raw, max.raw)
      axis(1, at=xv, labels=lv)
      if(scale=="row")
        mtext(side=1,"Row Z-Score", line=2)
      else if(scale=="column")
        mtext(side=1,"Column Z-Score", line=2)
      else
        mtext(side=1,"Value", line=2)

      if(density.info=="density")
        {
          ## Experimental : also plot density of data
          dens <- density(x, adjust=densadj, na.rm=TRUE)
          omit <- dens$x < min(breaks) | dens$x > max(breaks)
          dens$x <- dens$x[-omit]
          dens$y <- dens$y[-omit]
          dens$x <- scale01(dens$x,min.raw,max.raw)
          lines(dens$x, dens$y / max(dens$y) * 0.95, col=denscol, lwd=1)
          axis(2, at=pretty(dens$y)/max(dens$y) * 0.95, pretty(dens$y) )
          title("Color Key\nand Density Plot")
          par(cex=0.5)
          mtext(side=2,"Density", line=2)
        }
      else if(density.info=="histogram")
        {
          h <- hist(x, plot=FALSE, breaks=breaks)
          hx <- scale01(breaks,min.raw,max.raw)
          hy <- c(h$counts, h$counts[length(h$counts)])
          lines(hx, hy/max(hy)*0.95, lwd=1, type="s", col=denscol)
          axis(2, at=pretty(hy)/max(hy) * 0.95, pretty(hy) )
          title("Color Key\nand Histogram")
          par(cex=0.5)
          mtext(side=2,"Count", line=2)
        }
      else
        title("Color Key")

    }
  else
    plot.new()

  ## Create a table showing how colors match to (transformed) data ranges
  retval$colorTable <- data.frame(
                             low=retval$breaks[-length(retval$breaks)],
                             high=retval$breaks[-1],
                             color=retval$col
                             ) 

  
  invisible( retval )
}
