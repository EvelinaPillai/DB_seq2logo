import os
# For usage with ligando DB
from ligando.models import (
    DBSession,
    Base,
    PeptideRun
)
# For usage with Database if incorporated in ligando project
import paste.deploy
from sqlalchemy import engine_from_config

# Location to save logos
# SET OUTPUT DIR
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
output_dir = BASE_DIR + "/static/seqlogo/"

settings = paste.deploy.appconfig('config:' + os.path.join(BASE_DIR, '../', 'development.ini'))

engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)
Base.metadata.bind = engine


# Method to create Peptide binding motif by a list of peptides and filename
# peptides need the same length
def seq2logo_by_peptide_list(peptides, file_name):
    # write list to file
    # Note: peptides have to be trimmed to same length if query not already done
    # change peptide to peptide[1:9]
    peptide_file = open('peptide.txt', 'w')
    for peptide in peptides:
        peptide_file.write("%s\n" % peptide)
    peptide_file.close()

    os.system("./Seq2Logo.py  -I 1 -H ends --format PNG -f peptide.txt -o " + output_dir + file_name)

    # delete peptide file and unnecessary output afterwards
    os.remove("peptide.txt")
    os.remove(output_dir + file_name + ".txt")
    os.remove(output_dir + file_name + ".eps")
    os.remove(output_dir + file_name + "_freq.mat")

    # correct filename as seq2logo names logos "-001.png"
    old_file_name = output_dir + file_name + "-001.png"
    new_file_name = output_dir + file_name.split("-")[0]+".png"
    os.rename(old_file_name, new_file_name)


if __name__ == '__main__':
    # TODO right query for peptidelist and filename
    # Test query to get peptide list
    query = DBSession.query(PeptideRun.sequence)
    query = query.filter(PeptideRun.length >= 9).limit(1000)  # peptides must have same lenght

    # List of peptides for which one will create the Peptide binding motif-Logo
    peptide_list = query.all()
    filename = "A*01011"

    seq2logo_by_peptide_list(peptide_list, filename)