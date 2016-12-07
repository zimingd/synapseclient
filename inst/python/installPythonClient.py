import pip
import sys
import os
import urllib
import gzip
import tarfile
import shutil
import distutils.core

# install into <path>/inst/lib which will become the lib/ folder in the installed package
def main(path):
    moduleInstallationFolder=path+os.sep+"inst"
    sys.path.insert(0, moduleInstallationFolder)
    # The preferred approach is to use pip...
    pip.main(['install', '--user', 'urllib3',  '--upgrade'])
    pip.main(['install', '--user', 'requests',  '--upgrade'])
    pip.main(['install', '--user', 'six',  '--upgrade'])
    pip.main(['install', '--user', 'backports.csv',  '--upgrade'])
    
    # ...but - for some reason - pip breaks when we install future and the python synapse client
    # my guess is that pip 'shells out' to call setup.py and hops to another version of
    # python on the machine
    packageName = "future-0.15.2"
    linkPrefix = "https://pypi.python.org/packages/5a/f4/99abde815842bc6e97d5a7806ad51236630da14ca2f3b1fce94c0bb94d3d/"
    installPackage(packageName, linkPrefix, path)

    packageName = "synapseclient-1.6.1"
    linkPrefix = "https://pypi.python.org/packages/37/fd/5672e85abc68f4323e19e470cb7eeb0f8dc610566f124c930c3026404fb9/"
    installPackage(packageName, linkPrefix, path)
    
def installPackage(packageName, linkPrefix, path):
    # download 
    zipFileName = packageName + ".tar.gz"
    x = urllib.request.urlopen(linkPrefix+zipFileName)
    localZipFile = path+os.sep+zipFileName
    saveFile = open(localZipFile,'wb')
    saveFile.write(x.read())
    saveFile.close()

    tar = tarfile.open(localZipFile)
    tar.extractall(path=path)
    tar.close()
    os.remove(localZipFile)
    
    packageDir = path+os.sep+packageName
    sys.path.append(packageDir)
    os.chdir(packageDir)
    sys.argv=['setup.py', 'install', '--user'] 
    #TODO: this is a hacky solution. distutils.core.run_setup is supposed to be the one modifying sys.argv
    # it is able to do so on my local python but not on this compiled python
    # TODO how do we get 'setup.py' to install into inst/lib?
    distutils.core.run_setup(script_name='setup.py', script_args=['install', '--user'])
    
    
    # step back one level before remove the directory
    os.chdir(path)
    shutil.rmtree(packageDir)

