from typing import Dict, Tuple, Sequence,List
from plugins.ISpecialID import IStag,IDtag,IBtag,ITag
import re
import os
from shutil import copyfile,move,rmtree
class MyFile(IStag):
    kobj=None
    def getName(self) -> str:
        # self.kobj._write_to_stdout("setKernelobj setKernelobj setKernelobj\n")
        return 'MyFile'
    def getAuthor(self) -> str:
        return 'Author'
    def getIntroduction(self) -> str:
        return 'MyFile'
    def getPriority(self)->int:
        return 0
    def getExcludeID(self)->List[str]:
        return []
    def getIDSptag(self) -> List[str]:
        return ['file','saveto']
    def setKernelobj(self,obj):
        self.kobj=obj
        # self.kobj._write_to_stdout("setKernelobj setKernelobj setKernelobj\n")
        return
    def on_shutdown(self, restart):
        return
    def on_ISpCodescanning(self,key, value,magics,line) -> str:
        # return self.filehander(self,key, value,magics,line)
        try:
            self.kobj.addkey2dict(magics,'file')
            if len(value)>0:
                value=self.kobj.realpath(value)
                magics[key] += [value[re.search(r'[^/]',value).start():]]
            else:
                magics[key] +=['newfile']
        except Exception as e:
            self.kobj._log(str(e),2)
        return ''
    ##在代码预处理前扫描代码时调用    
    def on_Codescanning(self,magics,code)->Tuple[bool,str]:
        pass
        return False,code
    ##生成文件时调用
    def on_before_buildfile(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_buildfile(self,returncode,srcfile,magics)->bool:
        # self.kobj._log('on_after_buildfile  file\n',2)
        if len(self.kobj.addkey2dict(magics,'file'))>0:
            # self.kobj._log("srcfile:"+srcfile+"\n")
            newsrcfilename = self._fileshander(self,magics['file'],srcfile,magics)
            magics['codefilename']=newsrcfilename
            self.kobj._log("file "+ newsrcfilename +" created successfully\n")
        return False
    def on_before_compile(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_compile(self,returncode,binfile,magics)->bool:
        return False
    def on_before_exec(self,code,magics)->Tuple[bool,str]:
        return False,''
    def on_after_exec(self,returncode,srcfile,magics)->bool:
        return False
    def on_after_completion(self,returncode,execfile,magics)->bool:
        magics['file']=[]
        return False
    def filehander(self,key, value,magics,line):
        self.kobj._write_to_stdout(value+"\n")
        if len(value)>0:
            magics[str(key)] += [value[re.search(r'[^/]',value).start():]]
        else:
            magics[str(key)] +=['newfile']
        return ''
    def _fileshander(self,files:List,srcfilename,magics)->str:
        index=-1
        fristfile=srcfilename
        try:
            for newsrcfilename in files:
                index=index+1
                newsrcfilename = os.path.join(os.path.abspath(''),newsrcfilename)
                if os.path.exists(newsrcfilename):
                    if magics!=None and len(self.kobj.addkey2dict(magics,'overwritefile'))<1:
                        newsrcfilename +=(".new"+self.kobj.get_language_info()['file_extension'])
                if not os.path.exists(os.path.dirname(newsrcfilename)) :
                    os.makedirs(os.path.dirname(newsrcfilename))
                if index==0:
                    # content=self.kobj.readcodefile(srcfilename)
                    # with open(newsrcfilename, 'w',encoding="UTF-8") as codef1:
                    #     codef1.write(content)
                    #     codef1.flush()
                    move(srcfilename,newsrcfilename)
                    fristfile=newsrcfilename
                    files[0]=newsrcfilename
                else:
                    self.kobj._log("copy to :"+newsrcfilename+"\n")
                    copyfile(fristfile,newsrcfilename)
        except Exception as e:
                self.kobj._log(str(e),2)
        return files[0]
