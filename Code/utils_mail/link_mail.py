import re
from .meta_mail import meta_mail


def clean_subject_regex(subject):
    mailREGEX = "(Re|RE|FW) *([:] *)| *$"
    return re.sub(mailREGEX, "", subject)


def get_link_mails(df):
    subject_mail = {}
    for i in range(284, 285):
        subject = df["Subject"][i]
        clean_subject = clean_subject_regex(subject)
        if (clean_subject != "NoData" and clean_subject != "") and clean_subject not in subject_mail:
            relatedmail = get_all_mails(df, clean_subject)
            relatedmail2 = dispatch_mails(relatedmail)
            subject_mail[clean_subject] = relatedmail2
    return subject_mail


def get_all_mails(df, subject):
    mails = []
    for i in range(0, len(df.index)):

        if (subject in df['Subject'][i]):
            newSubject = clean_subject_regex(df['Subject'][i])

            if (newSubject in subject):
                tmp = {}
                tmp['id'] = df["Unnamed: 0"][i]
                tmp['Date'] = df['Date'][i]
                tmp['From'] = df['From'][i]
                tmp['To'] = df['To'][i]
                tmp['Subject'] = df['Subject'][i]
                # tmp['content'] = df['content'][i]
                # tmp['user'] = df['user'][i]
                mails.append(tmp)
    return mails


def dispatch_mails(related):
    dispatch = {}

    for i in range(0, len(related)):
        found = False
        j = 0
        courant = meta_mail(related[i])
        keys = list(dispatch)
        # while (found == False) and j < len(keys):
        #     #print(dispatch,len(dispatch))
        #     #print(keys)
        #     d = keys[j]
        #     print(keys[j])
        #     if courant.appartient(d):
        #         dispatch[d].append(related[i])
        #         found = True
        #     j = j + 1

        print(related[i])
        print(courant, dispatch, courant in dispatch)
        if courant in dispatch:
            dispatch[courant].append(related[i])
        else:
            dispatch[courant] = related[i]
        #
        # if(found == False):
        #     dispatch[courant] = related[i]

    return dispatch