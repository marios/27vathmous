Name:	discovery-dhcp-dnsmasq
Version:	0.0.1
Release:	1%{?dist}
Summary:	Creates a dedicated dnsmasq process for your undercloud, serving only unkown machines that are to go through autodiscovery.

Group:		
License:	ASL 2.0
URL:		http://github.com/agroup/instack-undercloud
Source0:
Source1:	discovery-dhcp-dnsmasq.service	
Source2:	discovery-mac-filter
Source3:	discovery-mac-filter-cronjob
Source4:	dnsmasq.conf


BuildArch:	noarch
BuildRequires:	systemd
BuildRequires:	dnsmasq
BuildRequires:	dnsmasq-utils

%description


%prep
%setup -q -n %{full_release}
<

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
#make the required directories:
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/tftpboot
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/cron.d
mkdir -p %{buildroot}/%{_sysconfdir}/discovery-dhcp
# install the discovery-mac-filter into /usr/bin:
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}
# install the cronjob to execute discovery-mac-filter every minute:
install -p -D -m 744 %{SOURCE3} %{buildroot}/%{_sysconfdir}/cron.d
# install discovery-dhcp-dnsmasq systemd service file
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir} 
#write out sample dnsmasq.conf
install -p -D -m 640 %{SOURCE4} %{buildroot}/%{_sysconfdir}/discovery-dhcp/


%files
%doc
/usr/bin/discovery-mac-filter
%{_unitdir}/discovery-dhcp-dnsmasq.service
%{_sysconfdir}/discovery-dhcp/dnsmasq.conf
%{_sysconfdir}/cron.d/discovery-mac-filter-cronjob

%post
%systemd_post discovery-dhcp-dnsmasq.service

%preun
%systemd_preun discovery-dhcp-dnsmasq.service

%postun
systemd_postun discovery-dhcp-dnsmasq.service

%changelog
