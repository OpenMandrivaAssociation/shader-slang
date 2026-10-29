# LTO of this compiler exhausts the builder memory budget.
%define _disable_lto 1
%global optflags %(echo %{optflags} | sed -e 's, -flto,,g')

Summary:	Slang shading language compiler
Name:		shader-slang
Version:	2026.18.3
Release:	2
License:	Apache-2.0 WITH LLVM-exception AND MIT
Group:		Development/Other
URL:		https://github.com/shader-slang/slang
Source0:	https://github.com/shader-slang/slang/archive/refs/tags/v%{version}.tar.gz#/slang-%{version}.tar.gz
# unordered_dense pin from v2026.18.3 external/unordered_dense
Source1:	https://github.com/martinus/unordered_dense/archive/73f3cbb237e84d483afafc743f1f14ec53e12314.tar.gz#/unordered_dense-73f3cbb237e84d483afafc743f1f14ec53e12314.tar.gz
# Lua pin used by the build-time slang-fiddle tool. onelua.c is not in system Lua.
Source2:	https://github.com/lua/lua/archive/3fe7be956f23385aa1950dc31e2f25127ccfc0ea.tar.gz#/lua-3fe7be956f23385aa1950dc31e2f25127ccfc0ea.tar.gz
# lib64 install paths, system cmark/glslang/spirv-tools, no libslang.so symlink.
Patch0:		shader-slang-openmandriva.patch

BuildRequires:	cmake(lz4) >= 1.10
BuildRequires:	cmake(miniz)
BuildRequires:	pkgconfig(libcmark-gfm)
BuildRequires:	cmake(FastFloat) >= 8.2
BuildRequires:	cmake(SPIRV-Headers)
BuildRequires:	cmake(VulkanHeaders)
BuildRequires:	cmake(glslang)
BuildRequires:	cmake(SPIRV-Tools)
BuildRequires:	cmake(SPIRV-Tools-opt)
BuildRequires:	cmake(SPIRV-Tools-link)

BuildSystem:	cmake
BuildOption:	-DSLANG_ENABLE_PCH=OFF
BuildOption:	-DSLANG_ENABLE_SLANG_GLSLANG=ON
BuildOption:	-DSLANG_ENABLE_SLANG_PROXY=OFF
BuildOption:	-DSLANG_ENABLE_SPLIT_DEBUG_INFO=OFF
BuildOption:	-DSLANG_ENABLE_EXAMPLES=OFF
BuildOption:	-DSLANG_ENABLE_TESTS=OFF
BuildOption:	-DSLANG_ENABLE_GFX=OFF
BuildOption:	-DSLANG_ENABLE_SLANG_RHI=OFF
BuildOption:	-DSLANG_ENABLE_DXIL=OFF
BuildOption:	-DSLANG_ENABLE_REPLAYER=OFF
BuildOption:	-DSLANG_ENABLE_XLIB=OFF
BuildOption:	-DSLANG_SLANG_LLVM_FLAVOR=DISABLE
BuildOption:	-DSLANG_INSTALL_USER_SKILLS=OFF
BuildOption:	-DSLANG_STANDARD_MODULE_DEVELOP_BUILD=OFF
BuildOption:	-DSLANG_USE_SYSTEM_MINIZ=ON
BuildOption:	-DSLANG_USE_SYSTEM_LZ4=ON
BuildOption:	-DSLANG_USE_SYSTEM_VULKAN_HEADERS=ON
BuildOption:	-DSLANG_USE_SYSTEM_SPIRV_HEADERS=ON
BuildOption:	-DSLANG_USE_SYSTEM_CMARK=ON
BuildOption:	-DSLANG_USE_SYSTEM_GLSLANG=ON
BuildOption:	-DSLANG_USE_SYSTEM_SPIRV_TOOLS=ON
BuildOption:	-DSLANG_ENABLE_CUDA=OFF
BuildOption:	-DSLANG_ENABLE_OPTIX=OFF
BuildOption:	-DSLANG_ENABLE_NVAPI=OFF
BuildOption:	-DSLANG_ENABLE_AFTERMATH=OFF
# OpenMandriva cmake turns RPATH off. slang-bootstrap runs from the build
# tree and has to find the compiler library next to it. Turn build RPATH
# back on, and still omit RPATH from the installed files.
BuildOption:	-DCMAKE_SKIP_RPATH:BOOL=OFF
BuildOption:	-DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON

%description
Slang is a shading language compiler for GPU programs. This package
ships the compiler driver, the language server, the interpreter, and
the compiler library. The bundled unordered_dense hash map is included
under the MIT license.

%prep -a
mkdir -p external/unordered_dense external/lua external/fast_float/include
tar -xf %{S:1} -C external/unordered_dense --strip-components=1
tar -xf %{S:2} -C external/lua --strip-components=1
ln -sfn %{_includedir}/fast_float external/fast_float/include/fast_float

%install -a
cp -a external/unordered_dense/LICENSE unordered_dense.LICENSE

%files
%license LICENSE unordered_dense.LICENSE
%{_bindir}/slang
%{_bindir}/slangc
%{_bindir}/slangd
%{_bindir}/slangi
%{_libdir}/libslang-compiler.so*
%{_libdir}/libslang-rt.so*
%{_libdir}/libslang-glsl-module-%{version}.so
%{_libdir}/libslang-glslang-%{version}.so
%{_libdir}/pkgconfig/slang-compiler.pc
%{_libdir}/cmake/slang/
%{_libdir}/slang-standard-module-%{version}/
%{_includedir}/slang*.h
