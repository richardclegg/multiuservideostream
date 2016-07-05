
file_var_names<-c("day","daysd","incost","incostsd",
    "betweencost","betweencostsd","outcost","outcostsd",
    "cpucost","cpucostsd", "totcost","totcostsd",
    "day2","sdday2","percman","percmansd", 
    "mandel","mandelsd","mandelsd2","mandelsd2sd",
    "totdel","totdelsd","totdelsd2","totdelsd2sd",
    "mq1","mq1sd","mq2","mq2sd","mq3","mq3sd","mq4","mq4sd","mq5","mq5sd",
    "uq1","uq1sd","uq2","uq2sd","uq3","uq3sd","uq4","uq4sd","uq5","uq5sd",
    "day3","sdday3", 
    "meansessno","meansessnosd",
    "sdsessno","sdsessnosd",
    "maxsessno","maxsessnosd",
    "meanusers","meanuserssd",
    "sdusers","sduserssd", 
    "maxusers","maxuserssd")

read_duration_file<-function(filename)
{
varnames<-c("duration",file_var_names)
plotdat<-read.table(filename,col.names=varnames)
plotdat$unmandel<-plotdat$totdel-plotdat$mandel
plotdat$unmandelsd<-sqrt(plotdat$totdelsd**2 + plotdat$mandelsd**2)
plotdat$unmandelsd2<-sqrt(plotdat$totdelsd2**2 + plotdat$mandelsd2**2)
plotdat$mandel<-plotdat$mandel/1000000
plotdat$unmandel<-plotdat$unmandel/1000000
plotdat$mandelsd<-plotdat$mandelsd/1000000
plotdat$unmandelsd<-plotdat$unmandelsd/1000000
plotdat$totdel<-plotdat$totdel/1000000
plotdat$totdelsd<-plotdat$totdelsd/1000000
plotdat
}

read_servers_file<-function(filename)
{
varnames<-c("noservers",file_var_names)
plotdat<-read.table(filename,col.names=varnames)
plotdat$unmandel<-plotdat$totdel-plotdat$mandel
plotdat$unmandelsd<-sqrt(plotdat$totdelsd**2 + plotdat$mandelsd**2)
plotdat$unmandelsd2<-sqrt(plotdat$totdelsd2**2 + plotdat$mandelsd2**2)
plotdat$mandel<-plotdat$mandel/1000000
plotdat$unmandel<-plotdat$unmandel/1000000
plotdat$mandelsd<-plotdat$mandelsd/1000000
plotdat$unmandelsd<-plotdat$unmandelsd/1000000
plotdat$totdel<-plotdat$totdel/1000000
plotdat$totdelsd<-plotdat$totdelsd/1000000
plotdat
}

read_users_file<-function(filename)
{
varnames<-c("nousers",file_var_names)
plotdat<-read.table(filename,col.names=varnames)
plotdat$unmandel<-plotdat$totdel-plotdat$mandel
plotdat$unmandelsd<-sqrt(plotdat$totdelsd**2 + plotdat$mandelsd**2)
plotdat$unmandelsd2<-sqrt(plotdat$totdelsd2**2 + plotdat$mandelsd2**2)
plotdat$totdelsd2<-plotdat$totdelsd2/1000000
plotdat$unmandelsd2<-plotdat$unmandelsd2/1000000
plotdat$mandelsd2<-plotdat$mandelsd2/1000000
plotdat$mandel<-plotdat$mandel/1000000
plotdat$unmandel<-plotdat$unmandel/1000000
plotdat$mandelsd<-plotdat$mandelsd/1000000
plotdat$unmandelsd<-plotdat$unmandelsd/1000000
plotdat$totdel<-plotdat$totdel/1000000
plotdat$totdelsd<-plotdat$totdelsd/1000000
plotdat$uoutcost<-plotdat$outcost/plotdat$nousers
plotdat$uoutcostsd<-plotdat$outcostsd/plotdat$nousers
plotdat$utotcost<-plotdat$totcost/plotdat$nousers
plotdat$utotcostsd<-plotdat$totcostsd/plotdat$nousers
plotdat$ubetweencost<-plotdat$betweencost/plotdat$nousers
plotdat$ubetweencostsd<-plotdat$betweencostsd/plotdat$nousers
plotdat
}


