#!/usr/local/bin/python
import os
# import ycm_core

# return the filename in the path without extension
def findFileName(path, ext):
  name = ''
  for projFile in os.listdir(path):
    # cocoapods will generate _Pods.xcodeproj as well
    if projFile.endswith(ext) and not projFile.startswith('_Pods'):
      name= projFile[:-len(ext):]
  return name

# WARNING!! No / in the end
def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )

def findProjectName(working_directory):
  projectName = findFileName(working_directory, '.xcodeproj')

  if len(projectName) <= 0:
    # cocoapod projects
    projectName = findFileName(working_directory, '.podspec')
  return projectName


flags = [
# TODO: find the correct cache path automatically
'-D__IPHONE_OS_VERSION_MIN_REQUIRED=80000',
'-miphoneos-version-min=9.3',
'-arch', 'arm64',
'-fblocks',
'-fmodules',
'-fobjc-arc',
'-fobjc-exceptions',
'-fexceptions',
'-isystem',
'/Library/Developer/CommandLineTools/usr/include/c++/v1', # for c++ headers <string>, <iostream> definition
'-x',
'objective-c',
# '-F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/Library/Frameworks',
# '-F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks',
# '-I/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/Foundation.framework/Headers',
# '-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
# '-isystem', '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1'
# '-I/Library/Developer/CommandLineTools/usr/include',
#custom definition, include subfolders
'-ProductFrameworkInclude', # include the framework in the products(in derivedData) folder
'-I./Example/'+findProjectName(DirectoryOfThisScript()), # new cocoapods directory
'-ISUB./Pod/Classes', # old cocoapods directory
'-ISUB./'+findProjectName(DirectoryOfThisScript()), # new cocoapods directory
# use headers in framework instead
#'-ISUB./Example/Pods', # new cocoapods directory
# '-F/Users/Lono/Library/Developer/Xcode/DerivedData/Scrapio-dliwlpgcvwijijcdxarawwtrfuuh/Build/Products/Debug-iphonesimulator/Kiwi/',
# '-include',
# './Example/Tests/Tests-Prefix.pch', # test project prefix header
'-isysroot', '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk'
# '-fencode-extended-block-signature',  #libclang may report error on this

# '-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/7.0.2/include', # let IncludeClangInXCToolChain handle it
# include-pch will make YouCompleteMe show 'no errors founded'
# '-include-pch',
# './Example/Tests/Tests-Prefix.pch', # test project prefix header

# modules failed trials
# '-fmodule-implementation-of',
# '-fimplicit-module-maps',
# '-F/Users/Lono/Library/Developer/Xcode/DerivedData/Scrapio-dliwlpgcvwijijcdxarawwtrfuuh/Build/Products/Debug-iphonesimulator/CocoaLumberjack',
# '-Wnon-modular-include-in-framework-module',
]

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# You can get CMake to generate this file for you by adding:
#   set( CMAKE_EXPORT_COMPILE_COMMANDS 1 )
# to your CMakeLists.txt file.
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

# if os.path.exists( compilation_database_folder ):
  # database = ycm_core.CompilationDatabase( compilation_database_folder )
# else:
# we don't use compilation database
database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def Subdirectories(directory):
  res = []
  for path, subdirs, files in os.walk(directory):
    for name in subdirs:
      item = os.path.join(path, name)
      res.append(item)
  return res

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def IncludeClangInXCToolChain(flags, working_directory):
  if not working_directory:
    return list( flags )

  new_flags = list(flags)
  # '-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/7.0.2/include',
  path = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/'
  clangPath = sorted_ls(path)[::-1] # newest file first

  includePath = ''
  if (len(clangPath) > 0):
    includePath = os.path.join('', *[path, clangPath[0], 'include'])
    new_flags.append('-I'+includePath)
  return new_flags

def FindDerivedDataPath( derivedDataPath, projectName ):
  simulatorPaths = ['Build/Intermediates/CodeCoverage/Products/Debug-iphonesimulator/', # if you enable CodeCoverage, the framework of test target will be put in coverage folder, strange
                    'Build/Intermediates/CodeCoverage/Products/Debug-iphoneos/',
                    'Build/Products/Debug-iphonesimulator/',
                    'Build/Products/Debug-iphoneos/']

  # search ~/Library/Developer/Xcode/DerivedData/ to find <project_name>-dliwlpgcvwijijcdxarawwtrfuuh
  derivedPath = sorted_ls(derivedDataPath)[::-1] # newest file first
  for productPath in derivedPath:
    if productPath.lower().startswith( projectName.lower() ):
      for simulatorPath in simulatorPaths:
        projectPath = os.path.join('', *[derivedDataPath, productPath, simulatorPath])
        if (len(projectPath) > 0) and os.path.exists(projectPath):
          return projectPath # the lastest product is what we want (really?)
  return ''

def IncludeFlagsOfFrameworkHeaders( flags, working_directory ):
  if not working_directory:
    return flags

  new_flags = []
  path_flag = '-ProductFrameworkInclude'
  derivedDataPath = os.path.expanduser('~/Library/Developer/Xcode/DerivedData/')

  # find the project name
  projectName = findProjectName(working_directory)
  if len(projectName) <= 0:
    return flags

  # add all frameworks in the /Build/Products/Debug-iphonesimulator/xxx/xxx.framework
  for flag in flags:
    if not flag.startswith( path_flag ):
      new_flags.append(flag)
      continue

    projectPath = FindDerivedDataPath( derivedDataPath, projectName )
    if (len(projectPath) <= 0) or not os.path.exists(projectPath):
      continue

    # iterate through all frameworks folders /Debug-iphonesimulator/xxx/xxx.framework
    for frameworkFolder in os.listdir(projectPath):
      frameworkPath = os.path.join('', projectPath, frameworkFolder)

      if not os.path.isdir(frameworkPath):
        continue

      once = False
      # the framework name might be different than folder name
      # we need to iterate all frameworks
      for frameworkFile in os.listdir(frameworkPath):
        if frameworkFile.endswith('framework'):

          # only add framework folder which actually contains frameworks
          if not once:
            # framwork folder '-F/Debug-iphonesimulator/<framework-name>'
            # solve <Kiwi/KiwiConfigurations.h> not found problem

            new_flags.append('-F'+frameworkPath)
            once = True
          # include headers '-I/Debug-iphonesimulator/xxx/yyy.framework/Headers'
          # allow you to use #import "Kiwi.h". NOT REQUIRED, but I am too lazy to change existing codes
          new_flags.append('-I' + os.path.join('', frameworkPath, frameworkFile,'Headers'))

  return new_flags


def IncludeFlagsOfSubdirectory( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_include_subdir = False
  path_flags = [ '-ISUB']
  for flag in flags:
    # include the directory of flag as well
    new_flag = [flag.replace('-ISUB', '-I')]

    if make_next_include_subdir:
      make_next_include_subdir = False
      for subdir in Subdirectories(os.path.join(working_directory, flag)):
        new_flag.append('-I')
        new_flag.append(subdir)

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_include_subdir = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        for subdir in Subdirectories(os.path.join(working_directory, path)):
            new_flag.append('-I' + subdir)
        break

    new_flags =new_flags + new_flag
  return new_flags

def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  #add include subfolders as well
  flags = IncludeFlagsOfSubdirectory( flags, working_directory )

  #include framework header in derivedData/.../Products
  flags = IncludeFlagsOfFrameworkHeaders( flags, working_directory )

  #include libclang header in xctoolchain
  flags = IncludeClangInXCToolChain( flags, working_directory )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )

import time
def FlagsForFile( filename, **kwargs ):
  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )

    # NOTE: This is just for YouCompleteMe; it's highly likely that your project
    # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
    # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
    # try:
      # final_flags.remove( '-stdlib=libc++' )
    # except ValueError:
      # pass
  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  # update .clang for chromatica every 5min TODO: very dirty
  chromatica_file = DirectoryOfThisScript() + '/.clang'

  if (not os.path.exists(chromatica_file)) or (time.time() - os.stat(chromatica_file).st_mtime > 5*60):
    parsed_flags = IncludeFlagsOfSubdirectory( final_flags, DirectoryOfThisScript() )
    escaped = [flag for flag in parsed_flags if " " not in flag] # chromatica doesn't handle space in flag
    f = open(chromatica_file, 'w') # truncate the current file
    f.write('flags='+' '.join(escaped))
    f.close()

  return {
    'flags': final_flags,
    'do_cache': True
  }


# if __name__ == "__main__":
  # print (FlagsForFile(""))

  # flags = [
  # '-D__IPHONE_OS_VERSION_MIN_REQUIRED=70000',
  # '-x',
  # 'objective-c',
  # '-ProductFrameworkInclude',
  # '-ProductFrameworkInclude',
  # '-F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/Library/Frameworks',
  # '-ISUB./Pods/Headers/Public',
  # '-MMD',
  # ]

  # print IncludeClangInXCToolChain(flags, DirectoryOfThisScript())
  # print IncludeFlagsOfFrameworkHeaders( flags, DirectoryOfThisScript() )

  # # res = subdirectory( DirectoryOfThisScript())
  # flags = [
  # '-D__IPHONE_OS_VERSION_MIN_REQUIRED=70000',
  # '-x',
  # 'objective-c',
  # '-F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/Library/Frameworks',
  # '-ISUB./Pods/Headers/Public',
  # '-MMD',
  # ]

  # print (IncludeFlagsOfSubdirectory( flags, DirectoryOfThisScript() ))
  # res = IncludeFlagsOfSubdirectory( flags, DirectoryOfThisScript() )
  # escaped = []
  # for flag in res:
    # if " " not in flag:
      # escaped.append(flag)
  # print ' '.join(escaped)
