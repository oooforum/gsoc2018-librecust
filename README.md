# LibreOffice customization and creation of legal Templates

Adding open source software in employee's workflow.

## Description

A set of modules, menu and toolbar customizations for LibreOffice Suite that ease the transition from Microsoft Office as well as ready to use templates that automate the creation of Greek Legal Documents. Those templates aim to encounter time consuming tasks by removing the formatting and layout procedures from employee workflow. Furthermore, an interface to access all those templates will be developed. All steps will be documented during the process and afterwards for future reference and development.

This project was suggested by [GFOSS - Open Technologies Alliance](https://gfoss.eu/home-posts/) in the context of [Google Summer of Code 2018](https://www.google.com).

## Implementation
Menu customizations are implemented by editing user configuration `.xml` files and adding UI functionality through predefined [dispatch commands](https://wiki.documentfoundation.org/Development/DispatchCommands) and macro scripts.
The must-see reference for LibreOffice Macro development that is of great use throughout this project is Andrew Pitonyak's [OpenOffice Macro Information](http://www.pitonyak.org/AndrewMacro.odt).

Modules and partially mockups will be implemented in `.ui` format mainly using [Glade](https://glade.gnome.org/). In the event of a feature that is not already implemented in LibreOffice (`.uno` files), we are going to use  [Libreoffice Software Development Kit 6.0](https://api.libreoffice.org/).

Then, we need to harvest Greek legal documents for template creation. Some relevant sources are websites of associations such as [EANDA](http://www.eanda.gr/) and [DSA](http://www.dsa.gr/). Those sources provide templates that do not have any specific format. Most of them are created by employees or lawyers thus their undefined structure.

Through this project, we will also create a "proof of concept" archive of templates using data and documents from several Greek court divisions as well as document the creation procedure of those templates and developed addons.

Templates will include "User defined fields" for static information (e.g. date and members of court) and "Bookmarks" for case specific info (e.g. description of law case) as well as properties for classification. Those can be tracked and used through the Java or Basic API as shown in LibreOffice [examples](https://api.libreoffice.org/examples/DevelopersGuide/Text/).

Finally, when the required "proof of concept" document archive is built, we will create templates for each one of them.

The document directory will be available for use through a LibreOffice extension. This extension will be an add-on (in the context of having a GUI built with LibreOffice Basic dialog editor).

The extension code acts as the backend part of our extension implementing functions that ease the access to LibreOffice Java API.

A large number of those functions are implemented (or inspired) by the following sources:
- Andrew Davison work on documenting Java Libreoffice Programming Concepts on [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/#contents)
- Samuel Mehrbrodt's repository for a basic Eclipse LibreOffice extension project [libreoffice-starter-extension](https://github.com/smehrbrodt/libreoffice-starter-extension)
-  Andrew D. Pitonyak's OpenOffice.org Macros Explained - [OOME Third Edition](http://www.pitonyak.org/OOME_3_0.pdf)

## Installing
During the development period of the project the installation procedure will be rather long. When sub-goals are implemented all steps will be included in an .oxt installation.

Installation requires running the installation bash script located at install_script/installer.sh

```bash
cd install_script
bash installer.sh
```
An interactive script asks the user for installation of required sub-modules of the project. Superuser permissions are required in some steps.

### Menubar Customization
1. Install required macro library from this [path](https://github.com/eellak/gsoc2018-librecust/blob/master/menu_customization/macros/LibreCustLib.oxt).
2. Install Greek language pack for LibreOffice `libreoffice-{fresh|still}-el`
3. Change Writer UI language to Greek from Tools->Options->Language Settings->Languages.
4. Close LibreOffice Writer
5. Backup your current menubar configuration
    ``` bash
    cd /home/user/.config/libreoffice/4/user/config/soffice.cfg/modules/swriter/menubar/
    cp menubar.xml menubar.xml.bak
    ```
6. Copy customized menubar.xml from this [path](https://github.com/eellak/gsoc2018-librecust/blob/master/menu_customization/menubar/menubar.xml) to previous .config path
7. Open LibreOffice Writer


## Mentors
Mentors overseeing the development process:
- Kostas Papadimas
- Theodoros Karounos

## Timeline
- [x] April 23 – May 14
* Building development environment while updating README and documentation for installation and packaging details.
* Harvesting of Greek legal documents and design of automation tools for template creation.
- [x] May 14 – May 20
* Creation of mockups and prototypes for specific MS Office details that are going to be implemented while getting feedback from users.
- [x] May 20 – June 15
* Implementation and testing of UI customizations.
* Development of Page Numbering extension in the context of easing UI workflow.
- [ ] June 15 – July 20
* Template development for a number of the harvested legal documents.
- [ ] July 20 – August 8
* Testing, adjustments and further documentation.
