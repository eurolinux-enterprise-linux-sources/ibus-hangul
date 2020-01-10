%global require_ibus_version 1.3.99
%global require_libhangul_version 0.1.0

Name:       ibus-hangul
Version:    1.4.2
Release:    5%{?dist}
Summary:    The Hangul engine for IBus input platform
License:    GPLv2+
Group:      System Environment/Libraries
URL:        http://code.google.com/p/ibus/
Source0:    http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
# upstreamed patches
#Patch0:     ibus-hangul-HEAD.patch
# not upstreamed patches
Patch1:     ibus-hangul-dconf-prefix.patch

BuildRequires:  gettext-devel, automake, libtool
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  libhangul-devel >= %{require_libhangul_version}
BuildRequires:  pkgconfig
BuildRequires:  ibus-devel >= %{require_ibus_version}
BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel

Requires:   ibus >= %{require_ibus_version}
Requires:   libhangul >= %{require_libhangul_version}
Requires:   pygobject3

%description
The Hangul engine for IBus platform. It provides Korean input method from
libhangul.

%prep
%setup -q
%patch1 -p1 -b .dconf-prefix

autopoint -f
AUTOPOINT='intltoolize --automake --copy' autoreconf -fi

%build
%configure --disable-static %{?_with_hotkeys}
# make -C po update-gmo
make %{?_smp_mflags}

%install
make DESTDIR=${RPM_BUILD_ROOT} install INSTALL="install -p"

rm -f ${RPM_BUILD_ROOT}%{_bindir}/ibus-setup-hangul
sed -i 's!^Exec=ibus-setup-hangul!Exec=%{_libexecdir}/ibus-setup-hangul!' ${RPM_BUILD_ROOT}%{_datadir}/applications/ibus-setup-hangul.desktop

desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/ibus-setup-hangul.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libexecdir}/ibus-engine-hangul
%{_libexecdir}/ibus-setup-hangul
%{_datadir}/ibus-hangul
%{_datadir}/ibus/component/*
%{_libdir}/ibus-hangul/setup/*
%{_datadir}/applications/ibus-setup-hangul.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Wed Jun 19 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-5
- Remove ibus-setup-hangul symlink in %%{_bindir}.
- Fix bogus changelog date.

* Tue Apr  2 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-4
- Fix the last update which didn't apply the patch.

* Tue Apr  2 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-3
- Remove have_bridge_hotkey and need_pygobject3 macros which does no
  longer make sense after F17
- Add ibus-hangul-dconf-prefix.patch
- Fix bug 909509 - Hangul Keybaord doesn't be changed in IBusHangul Setup

* Wed Mar 27 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-2
- Pull the latest config.guess and config.sub for ARM64 port

* Tue Jan 29 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-1
- Update version to 1.4.2.
- Remove ibus-hangul-setup-gi.patch

* Wed Nov 21 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-9
- Fix a typo (R: -> BR: python2-devel)

* Wed Nov 21 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-8
- Cleanup the spec file

* Thu Nov 15 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-7
- Re-add ibus-hangul-HEAD.patch based on recent upstream change
- Apply ibus-hangul-add-hangul-hotkey.patch only for F-15 and F-16

* Wed Oct 31 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-6
- Add ibus-hangul-engine-name.patch
- Update ibus-hangul-setup-gi.patch
- Fix bug 870318 - Change of “Automatic reordering” setup option
  cannot be applied in ibus-hangul setup (thanks Mike FABIAN for the patch)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  8 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-4
- Fix ibus-hangul-setup-gi.patch
- Remove previously applied ibus-hangul-setup-race-condition.patch
- Fix bug 828597 - [abrt] ibus-hangul-1.4.1-2.fc16:
  main.py:184:on_value_changed:TypeError: 'NoneType' object is not
  iterable

* Wed Jun  6 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-3
- Fix ibus-setup-hangul race condition
- Fix bug 828597 - [abrt] ibus-hangul-1.4.1-2.fc16:
  main.py:184:on_value_changed:TypeError: 'NoneType' object is not
  iterable

* Tue May  1 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-2
- Add pygobject3 to dependencies on F-16.
- Fix bug 816890 - [abrt] ibus-hangul-1.4.0-5.fc16:
  main.py:23:<module>:ImportError: No module named gi.repository

* Tue Apr 17 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-1
- Update version to 1.4.1.
- Check RHEL version as well as Fedora version.

* Tue Mar  6 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-5
- Revive <hotkey> in hangul.xml.
- Remove unnecessary BR: ibus.
- Port ibus-setup-hangul to use gobject-introspection.

* Mon Mar  5 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-4
- Package the latest git master.
- Fix bug 799776 - [abrt] ibus-hangul-1.4.0-3.fc17
- Remove upstreamed patches: ibus-hangul-xx-icon-symbol.patch,
  ibus-hangul-no-ibus-daemon.patch, and
  ibus-hangul-use-system-icon.patch

* Fri Feb 10 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-3
- Add ibus-hangul-use-system-icon.patch
- Fix bug 789230 - ibus hangul Icon missing in gnome-shell (fedora 17)

* Tue Jan 31 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-2
- Add ibus-hangul-no-ibus-daemon.patch.
- Fix bug 784377 - [abrt] ibus-hangul-1.4.0-1.fc16

* Thu Jan 12 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-1
- Update version to 1.4.0.
- Remove ibus-hangul-ibus-1.4.patch.
- Drop %%defattr(-,root,root,-) from %%files.
- Pass -p to install to preserve file timestamps.
- Install ibus-setup-hangul.desktop properly.

* Thu Nov 24 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-1
- Update version to 1.3.2.

* Mon Oct 24 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-8
- Rebuild with the latest libhangul.

* Fri Aug 19 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-7
- Enable --with-hotkeys for F16 or later.
- Fix bug 731913 - No Hangul Key in keyboard Shortcuts

* Mon Jul 18 2011 Daiki Ueno <ueno@unixuser.org> - 1.3.1-6
- Fix entity reference for icon symbol.
- Fix bug 722566 - Cannot select Hangul Input Method on Ibus Preferences

* Thu Jul  7 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-5
- Don't specify --with-hotkeys.

* Mon Jul  4 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-4
- Added ibus-hangul-xx-icon-symbol.patch to enable the engine symbol & hotkeys.

* Wed May 11 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-3
- Update ibus-1.4 patch.
- Move the ibus version check into the patch from this spec.
- Fix bug 695971 - Hangul Keybaord Layout works to only dubeolsik

* Mon Apr  4 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-2
- Apply ibus-1.4 patch conditionally for SRPM compatibility.
- Drop buildroot, %%clean and cleaning of buildroot in %%install

* Mon Feb 28 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-1
- Update version to 1.3.1.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.20100329-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-4
- Add ibus-hangul-gvariant.patch for ibus-1.3.99

* Mon Aug 23 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-3
- Update ibus-hangul-HEAD.patch

* Tue Aug  3 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-1
- Update version to 1.3.0.20100329
- Add ibus-hangul-HEAD.patch to synch it with the git master

* Thu Feb 04 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20100102-1
- Update version to 1.2.0.20100102
- Add ibus-hangul-phuang.patch for ibus-1.2.99

* Fri Dec 11 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20091031-1
- Update version to 1.2.0.20091031.
- Drop ibus-hangul-1.1.0.20090328-right-ctrl-hanja.patch and
  ibus-hangul-1.1.0.20090328-hanja-arrow-keys.patch temporarily, because
  patches conflict with 1.2.0.20091031, and the key configure will available
  in next release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090617-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090330-1
- Update version to 1.2.0.20090617.

* Sun Apr 12 2009 Warren Togami <wtogami@redhat.com> - 1.1.0.20090330-2
- Bug 493706: ibus-hangul Hanja arrow keys are wrong
- Bug 493509: ibus-hangul missing right Ctrl for Hanja button
  These fixes are not ideal, but they make it usable for Fedora 11.
  These must become configurable in a future version.

* Mon Mar 30 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090330-1
- Update version to 1.1.0.20090330.
- Fix bug 486056 - missing options for 2bul, 3bul and other Korean layouts
- Fix bug 487269 - missing Hanja Conversion

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0.20090211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090211-1
- Update version to 1.1.0.20090211.

* Thu Feb 05 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090205-1
- Update version to 1.1.0.20090205.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-2
- Rebuild for Python 2.6

* Thu Oct 23 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081023-1
- Update to 0.1.1.20081023.

* Tue Sep 09 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Fri Aug 08 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080823-1
- The first version.
