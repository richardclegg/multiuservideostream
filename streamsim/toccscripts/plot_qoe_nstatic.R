source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
    cat("Requires static static_moving no_users outputfile")
    return
}
filename1<- args[1]
filename2<-args[2]
nousers<- as.numeric(args[3])
outfilename<- args[4]

static<-read_servers_file(filename1)
statictime<-read_servers_file(filename2)



#cat(random$unmandel,"\n")
#cat(static$unmandel,"\n")
#cat(dynamic$unmandel,"\n")
#cat(dynamic$unmandel,"\n")

static$type<-"d"
statictime$type<-"e"
combined<-rbind(static,statictime)

col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)
linetypes<-c(1,3)
shapetypes<-c(15,16)
theme_opts <- theme_bw()



wid<-0.1
dodge<-c(wid*-1,0,wid)
minx<-min(static$noservers-wid*2)
maxx<-max(static$noservers+wid*2)
breaks<-as.numeric(levels(factor(static$noservers)))
g<-ggplot(combined,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1],ymin=mandel-2*mandelsd, ymax=mandel+2*mandelsd, colour="a"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=mandel,colour="a",linetype=type))+
    geom_point(aes(x=noservers+dodge[1],y=mandel,colour="a",shape=type)) + 
    geom_errorbar(aes(x=noservers+dodge[2],ymin=unmandel-2*unmandelsd, ymax=unmandel+2*unmandelsd, colour="b"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[2],y=unmandel,colour="b",linetype=type)) +
    geom_point(aes(x=noservers+dodge[2],y=unmandel,colour="b",shape=type)) +
    geom_errorbar(aes(x=noservers+dodge[3],ymin=totdel-2*totdelsd, ymax=totdel+2*totdelsd, colour="c"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[3],y=totdel,colour="c",linetype=type)) +
    geom_point(aes(x=noservers+dodge[3],y=totdel,colour="c",shape=type)) +
    scale_colour_manual(breaks=c("a","b","c"),
        values=allcols, labels=c("managed","unmanaged","total"),
        guide = guide_legend(title = element_blank())) +
    scale_linetype_manual(name="combined",breaks=c("d","e"),
        values=linetypes, labels=c("static","static/time")) +
    scale_shape_manual(name="combined",breaks=c("d","e"),
        values=shapetypes, labels=c("static","static/time")) +
    guides(linetype= 
        guide_legend(title=element_blank())) +
    guides(shape= 
        guide_legend(title=element_blank())) +
    xlab("Number of cloud hosts/session") +
    ylab("Mean delay (secs)")
ggsave(outfilename,width=6.0,height=2.05)
