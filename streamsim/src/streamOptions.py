#!/usr/bin/env python

import json
import sys

import demandmodel.demandModel as demandModel
import networkmodel.networkModel as networkModel
import qoemodel.qoeModel as qoeModel
import routemodel.routeModel as routeModel
import servermodel.serverModel as serverModel
import sessionmodel.sessionModel as sessionModel
import outputmodel.outputModel as outputModel

class streamOptions(object):

    def __init__(self):
        """Initialise the streamOptions class which contains
        the information read from the configuration file for
        the simulation"""
        self.outputFile= None
        self.routeMod= None
        self.sessionMod= None
        self.netMod= None
        self.demMod= None
        self.qoeMod= None
        self.serverMod= None
        self.outputs= []
        self.simDays= 0

    def readJson(self,fName):
        """Read a JSON file containing the options for the
        file and read any subsidiary files included in that
        file"""

        try:
            f= open(fName)

        except:
            print >> sys.stderr,'Cannot open',fName
            return False
        try:
            js=json.load(f)
        except ValueError as e:
            print >> sys.stderr, 'JSON parse error in',fName
            print >> sys.stderr, e
            sys.exit()
        f.close()
        try:
            outPart= js.pop('output')
        except:
            outPart= None
        try:
            sessModel= js.pop('session_model')
            dModel= js.pop('demand_model')
            nModel= js.pop('network_model')
            rModel= js.pop('route_model')
            qModel= js.pop('qoe_model')
            svrModel= js.pop('server_model')
            outputs= js.pop('output_models')
            self.simDays= js.pop('simulation_days')
        except ValueError as e:
            print >> sys.stderr, 'JSON file',fName, \
                'must contain stream_model, route_model' \
                'demand_model, network_model and simulation_days'
            return False
        if type(self.simDays) != int:
            print >> sys.stderr, 'JSON file',fName, \
                'must specify simulation_days as integer'
            return False
        if not self.checkJSEmpty(js,fName):
            return False
        try:
            if outPart != None:
                self.parseOutPart(outPart,fName)
            self.parseSessionModel(sessModel,fName)
            self.parseDemandModel(dModel,fName)
            self.parseNetworkModel(nModel,fName)
            self.parseRouteModel(rModel,fName)
            self.parseQoeModel(qModel,fName)
            self.parseServerModel(svrModel,fName)
            for o in outputs:
                self.outputs.append(self.parseOutputModel(o,fName))
        except ValueError as e:
            return False
        return True

    def checkJSEmpty(self,js,fName):
        if (len(js) != 0):
            print >> sys.stderr, 'JSON file',fName, \
                'contains unrecognised keys',js.keys()
            return False
        return True

    def parseOutPart(self,js,fName):
        """ Parse the output part of the stream model JSON config"""
        try:
            self.outputFile= js.pop('file')
        except:
            pass
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError



    def strToClassInstance(self,classStr,classType):
        """Convert string to a class instance"""
        try:
            (modName,_,className)= classStr.rpartition('.')
            newmodule= __import__(modName, fromlist=[''])
            objClass= getattr(newmodule,className)
        except AttributeError as e:
            print >> sys.stderr, "Making ",classStr,"into class",classType, \
                "Attribute Error", e
            raise ValueError("%s must be qualified class." % classStr)
        except ImportError as e:
            print >> sys.stderr, "Making ",classStr,"into class",classType, \
                "Attribute Error", e
            raise ValueError("Cannot find class %s module name %s to import"
                % (className,modName))
        obj= objClass()
        if isinstance(obj,classType):
            return obj
        raise ValueError("%s is not a valid class of type sessionModel." % classStr)

    def parseSessionModel(self,js,fName):
        """ Parse the session Model part of the stream model
        JSON config"""
        try:
            modelStr= js.pop('type')
        except:
            print >> sys.stderr,'JSON file',fName, \
                'must contain model_type'
        try:
            self.sessionMod= self.strToClassInstance(modelStr,
                sessionModel.sessionModel)
            self.sessionMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr,'JSON file',fName, \
                'has error with type in session_model'
            print >> sys.stderr, e
            raise e

        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError

    def parseDemandModel(self,js,fName):
        """ Parse the demand Model part of the stream model
        JSON config"""
        try:
            demModType= js.pop('type')
        except ValueError as e:
            print >> sys.stderr, "demand_model in JSON must contain" \
                "type in JSON ",fName
            raise e
        try:
            self.demMod= self.strToClassInstance(demModType,
                demandModel.demandModel)

        except ValueError as e:
            print >> sys.stderr,"JSON in demand_model has error with " \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            self.demMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in",\
                "demand_model in",fName
            print >> sys.stderr, "Error given:",e
            raise e
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError

    def parseNetworkModel(self, js, fName):
        """Parse the network model from the JSON"""
        try:
            netModType= js.pop('type')
        except Exception as e:
            print >> sys.stderr, "network_model in JSON must contain" \
                "type in JSON ",fName
            raise e
        try:
            self.netMod= self.strToClassInstance(netModType,
                networkModel.networkModel)
        except Exception as e:
            print >> sys.stderr,"JSON in network_model has error with" \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            self.netMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in ",\
                "network_model in",fName
            print >> sys.stderr, e
            raise e
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError

    def parseRouteModel(self, js, fName):
        """Parse the route model from the JSON"""
        try:
            routeModType= js.pop('type')
        except Exception as e:
            print >> sys.stderr, "route_model in JSON must contain" \
                "type in JSON ",fName
            raise e
        try:
            self.routeMod= self.strToClassInstance(routeModType,
                routeModel.routeModel)
        except Exception as e:
            print >> sys.stderr,"JSON in route_model has error with" \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            self.routeMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in ",\
                "route_model in",fName
            print >> sys.stderr, e
            raise e
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError

    def parseQoeModel(self, js, fName):
        """ Parse the model for user quality of experience from the
        JSON config input"""
        try:
            qoeModType= js.pop('type')
        except Exception as e:
            print >> sys.stderr, "qoe_model in JSON must contain" \
                "type in JSON ",fName
            raise e
        try:
            self.qoeMod= self.strToClassInstance(qoeModType,
                qoeModel.qoeModel)
        except ValueError as e:
            print >> sys.stderr,"JSON in qoe_model has error with", \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            self.qoeMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in ",\
                "qoe_model in",fName
            print >> sys.stderr, e
            raise e
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in file",fName
            raise ValueError

    def parseServerModel(self,js, fName):
        """Parse the model which learns about and assigns servers"""
        try:
            serverModType= js.pop('type')
        except Exception as e:
            print >> sys.stderr, "server_model in JSON must contain" \
                "type in JSON ",fName
            raise e
        try:
            self.serverMod= self.strToClassInstance(serverModType,
                serverModel.serverModel)
        except ValueError as e:
            print >> sys.stderr,"JSON in server_model has error with", \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            self.serverMod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in ",\
                "server_model in",fName
            print >> sys.stderr, e
            raise e
        if not self.checkJSEmpty(js,fName):
            print >> sys.stderr,"JSON contains unused tokens", js, \
                "in server_model in file",fName
            raise ValueError

    def parseOutputModel(self, js, fName):
        """Parse one of the models which gives output"""
        try:
            omType= js.pop('type')
        except Exception as e:
            print >> sys.stderr, "Every instance of output_models in JSON must contain" \
                "type ",fName
            raise e
        try:
            outputmod= self.strToClassInstance(omType,
                outputModel.outputModel)
        except ValueError as e:
            print >> sys.stderr,"JSON in server_model has error with", \
                "type in",fName
            print >> sys.stderr, e
            raise e
        try:
            outputmod.parseJSON(js,fName)
        except ValueError as e:
            print >> sys.stderr, "Parsing error with JSON in",\
                "output_models in",fName
            print >> sys.stderr, "Error given:",e
            raise e
        return outputmod
