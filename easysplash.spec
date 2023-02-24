%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define snapshot 20230224

Summary:	Tool for animated bootsplash screens
Name:		easysplash
Version:	1.0.0
Release:	0.%{snapshot}.1
Group:		System/Kernel and hardware
License:	GPL
Url:		https://github.com/OSSystems/EasySplash
# git clone https://github.com/OSSystems/EasySplash.git
# git archive --format=tar --prefix easysplash-1.0.0-$(date +%Y%m%d)/ HEAD | xz -vf > easysplash-1.0.0-$(date +%Y%m%d).tar.xz
Source:		%{name}-%{version}-%{snapshot}.tar.xz
ExclusiveArch:	%{rust_arches}
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(gstreamer-1.0)
%if %{__cargo_skip_build}
BuildArch:	noarch
%endif
BuildRequires:	rust-packaging
BuildRequires:	systemd-rpm-macros

%description
EasySplash is an application that runs early the OS boot
for showing graphical animation while the boot process
itself happens in the background.

%prep
%autosetup -p1 -n %{name}-%{version}-%{snapshot}

%build
%set_build_flags
export CARGO_PROFILE_RELEASE_DEBUG=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
export CARGO_PROFILE_RELEASE_INCREMENTAL=false
export CARGO_PROFILE_RELEASE_LTO=thin
export CARGO_PROFILE_RELEASE_OPT_LEVEL=z
export CARGO_PROFILE_RELEASE_PANIC=abort
export RUSTONIG_DYNAMIC_LIBONIG=1
cargo build --release --features systemd

%install
sed -i -e "s#@SYSCONFDIR@#%{_sysconfdir}#g" etc/%{name}*service.in
sed -i -e "s#@SBINDIR@#%{_bindir}#g" etc/%{name}*service.in
sed -i -e "s#/lib/easysplash#%{_datadir}/%{name}#g" ./etc/%{name}*service.in

install -m755 -D ./target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -m644 -D ./etc/%{name}.default %{buildroot}%{_sysconfdir}/default/%{name}
install -m644 -D ./etc/%{name}-start.service.in %{buildroot}%{_unitdir}/%{name}-start.service
install -m644 -D ./etc/%{name}-quit.service.in %{buildroot}%{_unitdir}/%{name}-quit.service
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a data/* %{buildroot}%{_datadir}/%{name}
# (tpg) set default animation
ln -sf %{_datadir}/%{name}/glowing-logo %{buildroot}%{_datadir}/%{name}/animation

%files
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}*.service
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
