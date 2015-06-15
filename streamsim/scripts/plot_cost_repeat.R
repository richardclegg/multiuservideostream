source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
    cat("Requires run1 run2 no_users outputfile")
}
filename1<- args[1]
filename2<-args[2]
nousers<- as.numeric(args[3])
outfilename<- args[4]


run1<-read_servers_file(filename1)
run2<-read_servers_file(filename2)


run1$utotcost<-run1$totcost/nousers
run1$utotcostsd<-run1$totcostsd/nousers
run2$utotcost<-run2$totcost/nousers
run2$utotcostsd<-run2$totcostsd/nousers



run1$type<-"d"
run2$type<-"e"

combined<-rbind(run1, run2)


col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)
linetypes<-c(1,3)
shapetypes<-c(15,16)
theme_opts<- theme_bw()



wid<-0.1
dodge<-c(wid*-1,wid)
minx<-min(combined$noservers-wid*2)
maxx<-max(combined$noservers+wid*2)
breaks<-as.numeric(levels(factor(combined$noservers)))
g<-ggplot(combined,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1],ymin=utotcost-2*utotcostsd, 
        ymax=utotcost+2*utotcostsd, colour=type), width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=utotcost,colour=type))+
    geom_point(aes(x=noservers+dodge[1],y=utotcost,colour=type)) +
    scale_colour_manual(breaks=c("d","e"),
        values=allcols, labels=c("run1","run2"),
        guide = guide_legend(title = element_blank())) + 
    xlab("Number of cloud hosts/session") +
    ylab("Mean cost per user $")
ggsave(outfilename,width=6.0,height=2.05)
