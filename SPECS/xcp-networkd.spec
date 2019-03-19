Name:           xcp-networkd
Version:        0.29.0
Release:        1%{?dist}
Summary:        Simple host network management service for the xapi toolstack
License:        LGPL
URL:            https://github.com/xapi-project/xcp-networkd
Source0:        https://code.citrite.net/rest/archive/latest/projects/XSU/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xcp-networkd/archive?at=v0.29.0&format=tar.gz&prefix=xcp-networkd-0.29.0#/xcp-networkd-0.29.0.tar.gz) = 5cacb077d199a6c2749c9d3695f6a177a9f02872
Source1:        xcp-networkd.service
Source2:        xcp-networkd-sysconfig
Source3:        xcp-networkd-conf
Source4:        xcp-networkd-network-conf
Source5:        init-xcp-networkd
BuildRequires:  libffi-devel
BuildRequires:  xs-opam-repo
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-xen-api-client-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  libnl3-devel
BuildRequires:  systemd-devel
Requires:       ethtool
Requires:       libnl3

%{?systemd_requires}

%description
Simple host networking management service for the xapi toolstack.

%prep
%autosetup -p1

%build
make

%install
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-networkd.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xcp-networkd
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xcp-networkd.conf
%{__install} -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xensource/network.conf
%{__install} -D -m 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/init.d/xcp-networkd

%files
%doc README.markdown LICENSE MAINTAINERS
%{_sbindir}/xcp-networkd
%{_bindir}/networkd_db
%{_unitdir}/xcp-networkd.service
%{_sysconfdir}/init.d/xcp-networkd
%{_mandir}/man1/xcp-networkd.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/xcp-networkd
%config(noreplace) %{_sysconfdir}/xcp-networkd.conf
%config(noreplace) %{_sysconfdir}/xensource/network.conf

%post
%systemd_post xcp-networkd.service

%preun
%systemd_preun xcp-networkd.service

%postun
%systemd_postun xcp-networkd.service

%changelog
* Mon Apr 09 2018 Christian Lindig <christian.lindig@citrix.com> - 0.29.0-1
- CA-287340: Slave reboot with unexpect enabled SRIOV.

* Thu Mar 22 2018 Marcello Seri <marcello.seri@citrix.com> - 0.28.0-1
- Add stub functions
- CP-26333 Implement Network.Interface.get_pci_bus_path
- Add more functions in Sysfs module and Ip module to support SRIOV.
- Add support for getting SRIOV capabilities.
- Add support for enabling SRIOV.
- Add support for disabling SRIOV.
- Add support for SRIOV VFs configuration.
- Use Astring instead of Xstring and fix whitespaces and format.
- CP-26856: unbind VFs from drivers before disable SR-IOV
- Port sriov to ppx
- CP-26923: Simplify Networkd logic by adding comments in modprobe config file.
- CA-285839: Fix return value if enabling SR-IOV via modprobe successful after reboot
- CA-286029: Disabling SR-IOV is failed on sysfs NIC
- CA-286290: Refine Configuring VF.
- CA-286290: A no-vlan SRIOV VIF shouldn't have a VLAN tag

* Wed Feb 28 2018 Christian Lindig <christian.lindig@citrix.com> - 0.27.0-1
- CP-26352 Port xcp-networkd from Camlp4 to PPX
- Convert configuration file to adapt `ipv4_route` structure changes

* Mon Feb 19 2018 Christian Lindig <christian.lindig@citrix.com> - 0.26.0-1
- jbuilder runtest: make it work when _build is not subdir of source root

* Fri Jan 19 2018 Christian Lindig <christian.lindig@citrix.com> - 0.25.0-1
- network_config, network_server: restore semantics of split

* Mon Dec 18 2017 Christian Lindig <christian.lindig@citrix.com> - 0.24.0-1
- Port to xapi-stdext-* submodules and Xstringext -> Astring
- Be explicit in the use of Xapi_stdext_pervasives.Pervasiveext
- Be more explicit in the use of Xapi_stdext_std.Listext
- Remove rtrim, replace with Astring.String.trim
- Use String.trim instead of Astring.String.trim when possible
- Compile with -safe-string
- CA-276745: Fix Networkd.Sysfs.get_driver_name
- Remove CLI

* Tue Dec 12 2017 Christian Lindig <christian.lindig@citrix.com> - 0.23.0-1
- CP-26156: Port xcp-networkd to use jbuilder
- rename package: xcp-networkd -> xapi-networkd

* Fri Oct 20 2017 Rob Hoes <rob.hoes@citrix.com> - 0.22.0-1
- CA-268679 XAPI loop report (Sys_error "Invalid argument")

* Thu Oct 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.21.0-1
- CA-196520: use mtu_request in OVS to set interface MTU

* Fri Sep 22 2017 Rob Hoes <rob.hoes@citrix.com> - 0.20.0-1
- CP-20569: Enable OVS IGMP Snooping by default
- CP-23093: Implement toggle of IGMP snooping on xcp-networkd
- CP-23601: Inject IGMP snooping query message when IGMP snooping toggle
- CP-23843: Disable IPv6 multicast snooping for OVS in XenServer
- CP-23835: Disable flooding of unregistered traffic
- CA-264980: Fork/exec igmp_query_injector.py and let it run in the background

* Mon Jul 03 2017 Rob Hoes <rob.hoes@citrix.com> - 0.19.0-1
- CA-244087: Update dhclient interface conf on changing default gateway.

* Thu Jun 01 2017 Rob Hoes <rob.hoes@citrix.com> - 0.18.0-1
- REQ-42: Support for management interface on a tagged VLAN

* Tue May 23 2017 Rob Hoes <rob.hoes@citrix.com> - 0.17.0-1
- CP-22405: Log message for config file not existing

* Thu May 18 2017 Rob Hoes <rob.hoes@citrix.com> - 0.16.0-1
- CP-22034: read PIF speed & duplex from sysfs; remove all the C bindings

* Wed Apr 26 2017 Rob Hoes <rob.hoes@citrix.com> - 0.15.0-1
- CA-250444: Always flush addresses when switching from DHCP to static

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 0.14.1-4
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Feb 23 2017 Gabor Igloi <gabor.igloi@citrix.com> - 0.14.1-3
- Depend upon xs-opam-repo providing updated OCaml libraries

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 0.14.1-2
- CA-243676: Do not restart toolstack services on RPM upgrade

* Thu Feb 09 2017 Rob Hoes <rob.hoes@citrix.com> - 0.14.1-1
- CA-223676: Add function `get_physical_interfaces` to networkd

* Wed Feb 08 2017 Rob Hoes <rob.hoes@citrix.com> - 0.14.0-1
- CA-239919: Avoid flushing static IPv4/v6 addresses when not needed

* Tue Dec 06 2016 Gabor Igloi <gabor.igloi@citrix.com> - 0.13.3-1
- CA-234506: Don't lose the port `kind` param in bridge.make_config

* Fri Nov 04 2016 Euan Harris <euan.harris@citrix.com> - 0.13.2-1
- CA-225272: rate-limit calls to `ovs-vsctl`

* Thu Oct 19 2016 Euan Harris <euan.harris@citrix.com> - 0.13.1-1
- CA-225365: Call mod-port on parent bridge, not "fake" VLAN bridge

* Thu Oct 13 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.13.0-1
- Update to 0.13.0

* Fri Sep 02 2016 Euan Harris <euan.harris@citrix.com> - 0.12.0-1
- Update to 0.12.0

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 0.11.1-2
- Package for systemd

* Fri Jul 22 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.11.1-1
- Update to 0.11.1

* Mon Jun 27 2016 Euan Harris <euan.harris@citrix.com> - 0.11.0-1
- Update to 0.11.0

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.9.6-1
- Re-run chkconfig on upgrade

* Wed Jun 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.4-1
- Update to 0.9.4
- Add networkd_db CLI

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Update to 0.9.3

* Wed Aug 28 2013 David Scott <dave.scott@eu.citrix.com>
- When loading the bridge module, prevent guest traffic being
  processed by the domain 0 firewall

* Sun Jun  9 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.2

* Fri Jun  7 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.1

* Wed Jun  5 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

