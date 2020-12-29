import json
import os.path
from os import path
import sys
import getopt
import time

# ---------------------
# Initial Config File
# ---------------------
ConfigFileName = 'Config'
InitailConfig = {'RootDirectiry': '',
                 'DtoDirectory': '',
                 'ServiseDirectory': '',
                 'ControllerDirectory': '',
                 }
# ---------------------------
# App Data
# ---------------------------
AppData = {'EntityName': '',
           'DtoName': '',
           'ServiceName': '',
           'ControllerName': '',
           'IsFull': 'false',
           'HasCreate': 'false',
           'HasCreateOrUpdate': 'false',
           'HasGet': 'false',
           'HasList': 'false',
           'HasDelete': 'false'
           }


class Cli:
    def __init__(self, RootDirectiry, DtoDirectory, ServiseDirectory, ControllerDirectory, EntityName, DtoName, ServiceName, ControllerName, IsFull, HasCreate, HasCreateOrUpdate, HasGet, HasList, HasDelete):
        self.RootDirectiry = RootDirectiry
        self.DtoDirectory = DtoDirectory
        self.ServiseDirectory = ServiseDirectory
        self.ControllerDirectory = ControllerDirectory
        self.EntityName = EntityName
        self.DtoName = DtoName
        self.ServiceName = ServiceName
        self.ControllerName = ControllerName
        self.IsFull = IsFull
        self.HasCreate = HasCreate
        self.HasCreateOrUpdate = HasCreateOrUpdate
        self.HasGet = HasGet
        self.HasList = HasList
        self.HasDelete = HasDelete
    pass

    def _start_(self):

        self._createDto_()
        self._cteateService_()
        self._unitOfWork_()
        self._IunitOfWork_()
        self._controller_()
        pass

    def _createDto_(self):
        _dto = self.RootDirectiry+'/'+self.DtoDirectory+'/'+self.DtoName+'.cs'
        _dtoDirectiry=self.DtoDirectory.replace("\\", ".")
        print(_dtoDirectiry)
        with open(_dto, 'w') as f:
            f.write('''
using System.Collections.Generic;
namespace %s
{
    public class %s
        {

        }
}''' % (_dtoDirectiry, self.DtoName)
                    )
            f.close()
        pass

    def _cteateService_(self):
        _service = self.RootDirectiry+'/'+self.ServiseDirectory+'/'+self.ServiceName+'.cs'
        _content='''
using AutoMapper;
using DAL.Models;
using ReposSrv.Repositories;

namespace Services
{
    public class %s:Repository<%s>
    {
        # region Fileds
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        # endregion
        # region Constructor
        public %s (SmartMonitoringContext Context, IUnitOfWork unitOfWork, IMapper mapper) : base(Context)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }
        # endregion
''' % (self.ServiceName, self.EntityName, self.ServiceName)

        if(self.HasGet=="true"):
            _content +='''
        #region Get
        public async Task<%s> Get(int id)
        {
            return null;
        } 
        #endregion
            '''%(self.DtoName)
            pass
        if(self.HasList=="true"):
            _content +='''
        public async Task<IEnumerable<%s>> List()
        {
            return null;
        }
            '''%(self.DtoName)
            pass
        if(self.HasCreate=="true"):
            _content +='''
        #region Create
        public async Task Create(%s model)
        {
            //var item = _mapper.Map<%s>(model);
            //Insert(item);
            await _unitOfWork.SaveChangesAsync();
        }
        #endregion
            '''%(self.DtoName,self.EntityName)
            pass
        if(self.HasCreateOrUpdate=="true"):
            _content +='''
        #region CreateOrUpdate
        public async Task CreateOrUpdate(%s model)
        {
            //var item = _mapper.Map<%s>(model);

            if (model.Id == null)
            {
                //Insert(item);
            }
            else
                //Update(item);

                await _unitOfWork.SaveChangesAsync();
        } 
        #endregion
            '''%(self.DtoName,self.EntityName)
            pass
        if(self.HasDelete=="true"):
            _content +='''
        #region Delete
        public async Task delete(int id)
        {
            Delete(new %s { Id = id });
            await _unitOfWork.SaveChangesAsync();
        } 
        #endregion
            '''%(self.EntityName)
            pass
        _content +='''
    }
}
        '''
        with open(_service, 'w') as f:
            f.write(_content )
            f.close()
        pass

    def _unitOfWork_(self):
        _unitOfWorkPath=self.RootDirectiry+"/"+self.ServiseDirectory+"/"+"UnitOfWork.cs"
        _content='''
        
        #region %s
        private IRepository<%s> _%s;

        public IRepository<%s> %s
        {
            get { return _%s = _%s ?? new %s(_context, this, _mapper); }
        }
        public %s %s => (%s)%s;
        #endregion
    }
}
'''%(self.ServiceName,self.EntityName,self.EntityName,self.EntityName,self.EntityName,self.EntityName,self.EntityName,self.ServiceName,self.ServiceName,self.ServiceName,self.ServiceName,self.EntityName)

        with open(_unitOfWorkPath, 'rb+') as f:
            f.seek(f.tell()-10,2)
            f.write(_content.encode('utf-8')  )
            f.close()
        pass

    def _IunitOfWork_(self):
        _IunitOfWorkPath=self.RootDirectiry+"/"+self.ServiseDirectory+"/"+"IUnitOfWork.cs"
        _content='''
        
        %s %s { get; }
        IRepository<%s> %s { get; }

    }
}
'''%(self.ServiceName,self.ServiceName,self.EntityName,self.EntityName)
        with open(_IunitOfWorkPath, 'rb+') as f:
            f.seek(f.tell()-10,2)
            f.write(_content.encode('utf-8')  )
            f.close()
        pass

    def _controller_(self):
        _controller = self.RootDirectiry+'/' + self.ControllerDirectory+'/'+self.ControllerName+'.cs'
        _content = '''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Common.Dtos.GuildUnionPollutions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Services;
using SSO.AuthenticateHandlers;
using Utilities;

namespace SmartMonitoring.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class %s : SSO.Core.Controllers.BaseController
    {
        # region Fileds
        private readonly IUnitOfWork _unitOfWork;

        # endregion

        # region Cunstractor
        public %s(IUnitOfWork unitOfWork, IJwtAuthenticationHandler iJWTValidatorService) : base(iJWTValidatorService)
        {
            _unitOfWork = unitOfWork;

        }
        # endregion
            ''' % (self.ControllerName, self.ControllerName)
        if(self.HasList == 'true'):
            _content += '''
        # region List
        [HttpGet("List")]

        public async Task<IActionResult> List()
        {
            try
            {
                var res = await this._unitOfWork.%s.List();
                return SuccessMessageHandler.SuccessfulResult(res);
            }
            catch (Exception e)
            {
                return await ErrorHandler.CustomBadRequest(e);
            }
        }
        # endregion
            ''' % (self.ServiceName)
            pass
        if(self.HasGet == 'true'):
            _content += '''
        # region Get
        [HttpGet("Get/{ id }")]

        public async Task<IActionResult> Get(int id)
        {
            try
            {
                var res = await this._unitOfWork.%s.Get(id);
                return SuccessMessageHandler.SuccessfulResult(res);
            }
            catch (Exception e)
            {
                return await ErrorHandler.CustomBadRequest(e);
            }
        }
        # endregion
             ''' % (self.ServiceName)
            pass  

        if(self.HasDelete=='true'):
            _content +='''
        # region Delete
        [HttpGet("Delete/{ Id }")]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                await this._unitOfWork.%s.delete(id);
                return SuccessMessageHandler.SuccessfulResult("Delete Sucsessful");
            }
            catch (Exception e)
            {
                return await ErrorHandler.CustomBadRequest(e);
            }
        }
        # endregion
               '''%(self.ServiceName)
            pass


        if(self.HasCreateOrUpdate=='true'):
            _content +='''
        # region CreateORUpdate
        [HttpPost("CreateOrUpdate")]
        public async Task<IActionResult> CreateOrUpdate(%s model)
        {
            try
            {
                var result = await this._unitOfWork.%s.CreateOrUpdate(model);
                return SuccessMessageHandler.SuccessfulResult("Cheange Sucseefuly Added ");
            }
            catch (Exception e)
            {
                return await ErrorHandler.CustomBadRequest(e);
            }
        }
        # endregion
             '''%(self.DtoName,self.ServiceName)
            pass

        if(self.HasCreate=="true"):
            _content +='''
        # region Create
        [HttpPost("Create")]
        public async Task<IActionResult> Create(%s model)
        {
            try
            {
                var result = await this._unitOfWork.%s.Create(model);
                return SuccessMessageHandler.SuccessfulResult("Cheange Sucseefuly Added");
            }
            catch (Exception e)
            {
                return await ErrorHandler.CustomBadRequest(e);
            }
        }
        # endregion

             '''%(self.DtoName,self.ServiceName)

            pass
        _content +='''
    }
}
        '''
        
        with  open(_controller, 'w') as f :
            f.write(_content)
            f.close()
        pass



pass


def main(argv):
    CheckArg(argv)
    InitailConfig=checkForConfig()
    cli=Cli(InitailConfig['RootDirectiry'],InitailConfig['DtoDirectory'],InitailConfig['ServiseDirectory'],InitailConfig['ControllerDirectory'],AppData['EntityName'], AppData['DtoName'], AppData['ServiceName'],AppData['ControllerName'],AppData['IsFull'],AppData['HasCreate'],AppData['HasCreateOrUpdate'],AppData['HasGet'],AppData['HasList'],AppData['HasDelete'])
    cli._start_()

pass

# -----------------------------
# If Config File Exist
# set config to app
# else Create config File
# -----------------------------
def checkForConfig():
    if path.exists(ConfigFileName):
        with open(ConfigFileName) as json_file:
            return  json.load(json_file)
        pass
    else:
        createConfig()
        pass
    pass


def createConfig():
    InitailConfig['RootDirectiry'] = input('\n \r Where is Root Directory : ')
    InitailConfig['DtoDirectory'] = input('\n \r Where is Dto Directory : ')
    InitailConfig['ServiseDirectory'] = input('\n \r Where is Servise Directory : ')
    InitailConfig['ControllerDirectory'] = input('\n \r Where is Controller Directory : ')
    with open(ConfigFileName, 'w') as outfile:
        json.dump(InitailConfig, outfile)
    pass


def CheckArg(argv):
    try:
        opts, args = getopt.getopt(argv, "h:e:dn:sn:cn:f:c:cu:g:l:d", ["Help=", "Entity=", "DtoName=", "ServiceName=", "ControllerName=", "IsFull=", "HasCreate=", "HasCreateUpdate=", "HasGet=", "HasList=", "Delete="])
    except getopt.GetoptError:
        print ('ooosa -h option for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ooosa -e <entitiy> -dn <dtoName> ....')
            print('-h --Help               for show how to use ')
            print('-e --Entity             your entity name')
            print('-d --DtoName            your Dto[ViewModel] name')
            print('-s --ServiceName        your Service name')
            print('-c --ControllerName     your Controller name')
            print('-f --IsFull             create Delete method in Controller')
            print('-a --HasCreate          create Create method in Controller')
            print('-w --HasCreateUpdate    create CreateUpdate method in Controller')
            print('-g --HasGet             create Get method in Controller')
            print('-l --HasList            create List method in Controller')
            print('-d --Delete             create Delete method in Controller ')
            sys.exit()

        elif opt in ("-e", "--Entity"):
            AppData['EntityName']=arg

        elif opt in ("-dn", "--DtoName"):
            AppData['DtoName']=arg

        elif opt in ("-sn", "--ServiceName"):
            AppData['ServiceName']=arg

        elif opt in ("-cn", "--ControllerName"):
            AppData['ControllerName']=arg

        elif opt in ("-f", "--IsFull"):
            AppData['IsFull']=arg
            AppData['HasCreate']='false'
            AppData['HasCreateOrUpdate']='true'
            AppData['HasGet']='true'
            AppData['HasList']='true'
            AppData['HasDelete']='true'

        elif opt in ("-c", "--HasCreate"):
            AppData['HasCreate']='true'
            AppData['HasCreateOrUpdate']='false'

        elif opt in ("-cu", "--HasCreateUpdate"):
            AppData['HasCreateOrUpdate']='true'
            AppData['HasCreate']='false'

        elif opt in ("-g", "--HasGet"):
            AppData['HasGet']='true'

        elif opt in ("-l", "--HasList"):
            AppData['HasList']='true'

        elif opt in ("-d", "--HasDelete"):
            AppData['HasDelete']='true'
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
