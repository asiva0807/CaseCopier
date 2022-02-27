import os
import sys
import getpass
import subprocess as sp

def RunCmd(fName,fType,TgtDir):
 if fType == ".tar.gz":
  fNameDir = fName.split(".tar.gz")[0]
 elif fType == ".tgz":
  fNameDir = fName.split(".tgz")[0]
 TgtDirIn = TgtDir + "/" + fNameDir
 os.system("pwd")
 os.system("mkdir "+TgtDirIn)
 os.system("chmod 777 "+TgtDirIn)
 os.system("mv "+fName+" "+fNameDir)
 os.chdir(TgtDirIn)


def getTGZFile(Lst):
 retFile={}
 for FName in Lst:
  if FName.endswith("tgz"):
   retFile[FName]=".tgz"
  elif FName.endswith("tar.gz"):
   retFile[FName]=".tar.gz" 
 return(retFile)


if len(sys.argv) == 1:
 sys.exit("Minimum variable needed - pls enter the case number")

yr = sys.argv[1][0:4]

UName = getpass.getuser()
dirCh = 0
BaseDir = "/volume/CSdata/"+UName+"/"+yr+"/"
#Check if year directory is under your CSData directory
if os.system("cd "+BaseDir) != 0:
 print("Creating directory : %s" % yr)
 os.system("mkdir "+BaseDir)
 os.system("chmod 777 "+BaseDir)

BaseCaseDir = "/volume/case_"+yr+"/"
CsNo = sys.argv[1] 
TgtDir = BaseDir+str(CsNo)
TgtCaseDir = BaseCaseDir+str(CsNo)
chkDir = "cd "+TgtDir
chkCaseDir = "cd "+TgtCaseDir

#EXCEPTION on wrong case number
if os.system(chkCaseDir) != 0:
 print("Invalid case Number %s or Customer has not uploaded logs for this case yet" % sys.argv[1])
 sys.exit("Script execution complete")

#EXCEPTION on preexisting directory
if os.system(chkDir) == 0:
 print("The case %s content is already in the desired location" % sys.argv[1])
 sys.exit("Delete the existing folder if needed")

#Copy operations   
print("__________________________ /n STARTING FILE TRANSFER /n _________________________________")
cmdLst = ['mkdir '+TgtDir,'chmod 777 '+TgtDir,'cd '+TgtDir,'cp '+TgtCaseDir+"/* ."]
if os.system(chkDir) == 512 and os.system(chkCaseDir) == 0:
 for cmd in cmdLst:
  if "cd" not in cmd:
   os.system(cmd)
  else:
   os.chdir(TgtDir)
   dirCh = 1
print("---------------------------------/n TRANSFER COMPLETE /n/n ---------------------------------")
if dirCh:
 FileLst = sp.getoutput("ls").split("\n")

TgzFlName = getTGZFile(FileLst)
print("******************************************************************************************************************************************")
print("Uncompressing Compressed file list : \t", TgzFlName)
print("******************************************************************************************************************************************")

for fName,fType in TgzFlName.items():
 if fType == ".tar.gz":
  print("############     EXTRACT TAR GZ FILE    ###################")
  RunCmd(fName,fType,TgtDir)
  os.system("gunzip "+fName)
  fName = sp.getoutput("ls").split("\n")[0]
 elif fType == ".tgz":
  print("###########      EXTRACT TGZ FILE    #######################")
  RunCmd(fName,fType,TgtDir)
 os.system("tar -xvf "+fName)
 os.chdir(TgtDir)


print("________________ END OF OPERATION _______________")

sivaa@svl-jtac-lnx05:~$ 