from lycee import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
import pymysql

class ApplicationIHM(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.score = 0
        self.fill_combobox_3()
        self.fill_combobox()
        self.fill_combobox_2()
        self.fill_combobox_4()
        self.fill_combobox_5()

    def fill_linedit_2(self):
        eleve = self.ui.comboBox_4.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from eleves where nom = '{eleve}'"
        requete = f"select Classe from classes where id_classe in( {id_classe})"
        cur.execute(requete)
        classe = cur.fetchall()[0][0]
        con.close()
        self.ui.lineEdit_2.setText(classe)

    def fill_combobox_4(self):
        self.ui.comboBox_4.clear()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        requete = "select nom from eleves"
        cur.execute(requete)
        eleves = cur.fetchall()
        con.close()
        index = 1
        for eleve in eleves:
            self.ui.comboBox_4.insertItem(index, eleve[0])
            index += 1

    def fill_combobox_3(self):
        self.ui.comboBox_3.clear()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        requete = "select Classe from classes"
        cur.execute(requete)
        classes = cur.fetchall()
        con.close()
        self.ui.comboBox_3.clear()
        index = 1
        for classe in classes:
            self.ui.comboBox_3.insertItem(index, classe[0])
            index += 1

    def fill_combobox(self):
        self.ui.comboBox.clear()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        cur.execute('SELECT nom FROM disciplines')
        resultat = cur.fetchall()
        con.close()
        index = 1
        for nom in resultat:
            self.ui.comboBox.insertItem(index, nom[0])
            index += 1

    def fill_combobox_2(self):
        self.ui.comboBox_2.clear()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        cur.execute('SELECT nom FROM profs')
        resultat = cur.fetchall()
        con.close()
        index = 1
        for nom in resultat:
            self.ui.comboBox_2.insertItem(index, nom[0])
            index += 1

    def eleve(self):
        self.fill_linedit_2()
        self.fill_etudes()
        self.fill_notes()


    def prof(self):
        self.fill_disciplines()
        self.fill_classes()
        self.fill_cours()

    def classe(self):
        self.fill_eleves()
        self.fill_professeurs()
        self.fill_discipline()

    def notes_classes(self):
        self.fill_combobox_6()
        self.fill_combobox_7()
        self.fill_combobox_8()

    def get_id_cours(self):
        index_cours1 = self.ui.comboBox_7.currentText()
        id = ''
        for c in index_cours1:
            if c == ' ':
                break
            else:
                id += c
        if id:
            id_cours = int(id)
        else:
            id_cours = 0
        return id_cours

    def fill_combobox_8(self):
        id_cours = self.get_id_cours()
        classe = self.ui.comboBox_5.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        requete = f"select id_devoir, date from devoirs where id_cours = {id_cours}"
        cur.execute(requete)
        devoirs = cur.fetchall()
        self.ui.comboBox_8.clear()
        index = 1
        for devoir in devoirs:
            item = f"{devoir[0]}  {devoir[1]}"
            self.ui.comboBox_8.insertItem(index, item)

    def get_id_devoir(self):
        index_devoir_1 = self.ui.comboBox_8.currentText()
        id = ''
        for c in index_devoir_1:
            if c == ' ':
                break
            else:
                id += c
        if id != '':
            id_devoir = int(id)
        else:
            id_devoir = 0
        return id_devoir

    def get_eleve_nom(self):
        eleve1 = self.ui.comboBox_6.currentText()
        eleve = ''
        for c in eleve1:
            if c == ' ':
                break
            else:
                eleve += c
        return eleve

    def get_id_eleve(self):
        eleve1 = self.ui.comboBox_6.currentText()
        eleve = ''
        for c in eleve1:
            if c == ' ':
                break
            else:
                eleve += c
        id_eleve = int(eleve)
        return id_eleve



    def get_single_note(self):
        id_devoir = self.get_id_devoir()
        eleve = self.get_eleve_nom()

        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        cur.execute(f"select id_eleve from eleves where nom = '{eleve}'")
        resultat = cur.fetchall()
        if resultat:
            id_eleve = resultat[0][0]
        else:
            id_eleve = 0

        requete = f"select note, id_note from notes where id_eleve = '{id_eleve}' " \
                  f"and id_devoir = {id_devoir}"
        cur.execute(requete)
        note = cur.fetchall()
        cur.close()
        if (note == ()):
            return None
        else:
            return note[0][0], note[0][1]

    def update_note(self):
        note = self.get_single_note()
        if (note == None):
            affichage = ''
        else:
            affichage = str(note[0])

        self.ui.lineEdit_3.setText(affichage)

    def add_change_note(self):
        print("gtrt")
        note = self.get_single_note()
        print(note)
        if note == None:
            self.add_single_note()
        else:
            self.update_single_note()

    def update_single_note(self):
        nouvelle_note = int(self.ui.lineEdit_3.text())
        print("nouvelle note ", nouvelle_note)
        ancienne_note = self.get_single_note()
        if ancienne_note != None:
            ancienne_note_id = ancienne_note[1]
        else:
            ancienne_note_id = 0
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        request = f"update notes set note = {nouvelle_note} where id_note = {ancienne_note_id}"
        cur.execute(request)
        print(cur.fetchall())
        con.commit()
        con.close()


    def add_single_note(self):
        print("new note")
        nouvelle_note = int(self.ui.lineEdit_3.text())
        id_devoir = self.get_id_devoir()
        id_eleve = self.get_id_eleve()
        print(f"id_eleve {id_eleve}  id_devoir {id_devoir}")
        if id_eleve and id_devoir:
            requete = f"insert into notes (  id_eleve, id_devoir, note) values ({id_eleve}, " \
                      f"{id_devoir}, {nouvelle_note})"
            con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
            cur = con.cursor()
            print(requete)
            cur.execute(requete)
            con.commit()
            con.close()

    def add_devoir(self):
        date = self.ui.lineEdit_4.text()
        print(date)
        id_cours = self.get_id_cours()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        requete = f"insert into devoirs (id_cours, date, description) " \
                  f"values ({id_cours}, '{date}', '')"
        print(requete)
        cur.execute(requete)
        con.commit()
        cur.close()

    def update_devoirs(self):
        self.fill_combobox_8()
        self.update_note()

    def fill_combobox_5(self):
        requete = "select Classe from classes"
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        cur.execute(requete)
        classes = cur.fetchall()
        self.ui.comboBox_5.clear()
        index = 1
        for classe in classes:
            self.ui.comboBox_5.insertItem(index, classe[0])
            index += 1
        con.close()

    def fill_notes(self):
        eleve = self.ui.comboBox_4.currentText()
        id_eleve = f"select id_eleve from eleves where nom = '{eleve}'"
        id_notes = f"select id_note from notes where id_eleve in ({id_eleve})"
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        requete = f"SELECT notes.note, disciplines.nom, profs.nom FROM " \
                  f"notes, disciplines, profs, devoirs, cours where " \
                  f"notes.id_note in ({id_notes}) " \
                  f"and notes.id_devoir = devoirs.id_devoir " \
                  f"and devoirs.id_cours = cours.id_cours " \
                  f"and cours.id_prof = profs.id_prof " \
                  f"and cours.id_discipline = disciplines.id_discipline"
        cur.execute(requete)
        notes = cur.fetchall()
        self.ui.listWidget_9.clear()
        for note in notes:
            item = str(note[0]) + "  " + note[1] + "  " + note[2]
            self.ui.listWidget_9.addItem(item)
        con.close()

    def fill_etudes(self):
        eleve = self.ui.comboBox_4.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from eleves where nom = '{eleve}'"
        id_cours = f"select id_cours from cours where id_classe in ({id_classe})"
        requete = f"select disciplines.nom, profs.nom from disciplines, profs, cours where" \
                  f" cours.id_cours in ({id_cours}) " \
                  f"and disciplines.id_discipline = cours.id_discipline " \
                  f"and cours.id_prof = profs.id_prof"
        cur.execute(requete)
        cours = cur.fetchall()
        self.ui.listWidget_8.clear()
        for cour in cours:
            item = cour[0] + "  " + cour[1]
            self.ui.listWidget_8.addItem(item)
        con.close()

    def fill_discipline(self):
        classe = self.ui.comboBox_3.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from classes where Classe = '{classe}'"
        id_disciplines = f"select id_discipline from cours where id_classe in ({id_classe})"
        requete = f"select nom from disciplines where id_discipline in ({id_disciplines})"
        cur.execute(requete)
        disciplines = cur.fetchall()
        self.ui.listWidget_7.clear()
        for discipline in disciplines:
            self.ui.listWidget_7.addItem(discipline[0])
        con.close()


    def fill_professeurs(self):
        classe = self.ui.comboBox_3.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from classes where Classe = '{classe}'"
        id_profs = f"select id_prof from cours where id_classe in ({id_classe})"
        requete = f"select nom, prenom from profs where id_prof in ({id_profs})"
        cur.execute(requete)
        profs = cur.fetchall()
        self.ui.listWidget_6.clear()
        for prof in profs:
            item = prof[0] + "  " + prof[1]
            self.ui.listWidget_6.addItem(item)
        con.close()


    def fill_eleves(self):
        classe = self.ui.comboBox_3.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from classes where Classe = '{classe}'"
        requete = f"select nom, prenom from eleves where id_classe in ({id_classe})"
        cur.execute(requete)
        eleves = cur.fetchall()
        self.ui.listWidget_5.clear()
        for eleve in eleves:
            nom = eleve[0]
            prenom = eleve[1]
            item = nom + "  " + prenom
            self.ui.listWidget_5.addItem(item)
        con.close()

    def fill_combobox_6(self):
        classe = self.ui.comboBox_5.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from classes where Classe = '{classe}'"
        requete = f"select id_eleve, nom, prenom from eleves where id_classe in ({id_classe})"
        cur.execute(requete)
        eleves = cur.fetchall()
        self.ui.comboBox_6.clear()
        index = 1
        for eleve in eleves:
            item = str(eleve[0]) + " " + eleve[1] +"  " + eleve[2]
            self.ui.comboBox_6.insertItem(index, item)
            index += 1
        con.close()

    def fill_combobox_7(self):
        classe = self.ui.comboBox_5.currentText()
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        id_classe = f"select id_classe from classes where Classe = '{classe}'"
        requete = f"select cours.id_cours, disciplines.nom, profs.nom " \
                  f"from disciplines, profs, cours where cours.id_classe in ({id_classe}) " \
                  f"and disciplines.id_discipline = cours.id_discipline " \
                  f"and profs.id_prof = cours.id_prof"
        cur.execute(requete)
        cours = cur.fetchall()
        self.ui.comboBox_7.clear()
        index = 1
        for cour in cours:
            item = str(cour[0])+ " "+ cour[1]+"  "+ cour[2]
            self.ui.comboBox_7.insertItem(index, item)
            index += 1
        con.close()

    def fill_cours(self):
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        prof = self.ui.comboBox_2.currentText()
        id_profs = f"select id_prof from profs where nom ='{prof}'"
        id_cours = f"select id_cours from cours where id_prof in ({id_profs})"
        description = f"select id_classe, id_discipline from cours " \
                      f"where id_cours in ({id_cours})"
        cur.execute(description)
        cours = cur.fetchall()
        self.ui.listWidget_4.clear()
        for cour in cours:
            id_classe = cour[0]
            id_discipline = cour[1]
            cur.execute(f'select Classe from classes where id_classe = {id_classe}')
            classe = cur.fetchall()[0][0]
            cur.execute(f'select nom from disciplines where id_discipline = {id_discipline}')
            discipline = cur.fetchall()[0][0]
            item = discipline + "  "+classe
            self.ui.listWidget_4.addItem(item)
        con.close()

    def fill_disciplines(self):
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        prof = self.ui.comboBox_2.currentText()
        requete = f'SELECT id_prof FROM profs WHERE nom = "{prof}"'
        requete = f'select id_discipline from cours where id_prof in({requete})'
        requete = f'select nom from disciplines where id_discipline in ({requete})'
        cur.execute(requete)
        disciplines = cur.fetchall()
        self.ui.listWidget_2.clear()
        for discipline in disciplines:
            self.ui.listWidget_2.addItem(discipline[0])
        con.close()

    def fill_classes(self):
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        prof = self.ui.comboBox_2.currentText()
        requete = f'SELECT id_prof FROM profs WHERE nom = "{prof}"'
        requete = f'select id_classe from cours where id_prof in({requete})'
        requete = f'select Classe from classes where id_classe in ({requete})'
        cur.execute(requete)
        classes = cur.fetchall()
        self.ui.listWidget_3.clear()
        for classe in classes:
            self.ui.listWidget_3.addItem(classe[0])
        con.close()

    def profs_par_discipline(self):
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        discipline = self.ui.comboBox.currentText()
        requete = 'SELECT id_discipline FROM disciplines WHERE nom = "'+discipline+'"'
        cur.execute(requete)
        resultat = cur.fetchall()
        if resultat:
            id_discipline = resultat[0][0]
        else:
            id_discipline = 0
        requete = f"select id_prof from cours where id_discipline = {id_discipline}"
        requete = f"select nom from profs where id_prof in ({requete})"
        cur.execute(requete)
        resultat = cur.fetchall()
        con.close()
        self.ui.listWidget.clear()
        for prof in resultat:
            self.ui.listWidget.addItem(prof[0])

    def add_discipline(self):
        nom = self.ui.lineEdit.text()
        requete = f"INSERT INTO disciplines (nom) VALUES ('{nom}')"
        con = pymysql.connect('localhost', 'kemar', '', 'projet_notes')
        cur = con.cursor()
        cur.execute(requete)
        cur.execute('select * from disciplines')
        con.commit()
        con.close()
        index = self.ui.comboBox.count()+1
        self.ui.comboBox.insertItem(index, nom)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationIHM()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
