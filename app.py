# app.py
import os, re, requests
from flask import Flask, render_template, redirect, url_for, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
#from dotenv import load_dotenv #where the bot token is stored locally, not used over Heroku 'os.environ.get' instead
from unidecode import unidecode #removes accented characters
from metaphone import doublemetaphone #converts a name into phonetics, allows for fuzzy name searching

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/slack_uID_db')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

slack_db = db.student_slack

'''slack_db.delete_many({})
slack_db.insert_many([{
    'ATMPRS': ('U1D40QFD4', 'Adam Braus'), 'ALNTFS': ('U1HBKMW8Y', 'Alan Davis'), 'KNMK': ('U1NCM4VME', 'Mike Kane'), 'LPRMKL': ('U1T2Q3G81', 'Michael Loubier'), 'LPRMXL': ('U1T2Q3G81', 'Michael Loubier'), 'PLXNN': ('U1U2T6HT6', 'Shannon Bailey'), 'KRLSTS': ('U1UTEGPU6', 'Carlos Diez'), 'KSSPNSR': ('U1VDXDV0X', 'Casey Spencer'), 'LMPRTSS': ('U1YM6H8MA', 'Tassos Lambrou'), 'JRMRSMN': ('U237ELPUH', 'Jeremy Rossmann'), 'ARMRSMN': ('U237ELPUH', 'Jeremy Rossmann'), 'TSKML': ('U2481KKBM', 'Komal Desai'), 'PPTKRT': ('U264ANGAE', 'Bob De Kort'), 'HTSNMXL': ('U28S64ZJ5', 'Mitchell Hudson'), 'NSPTSSN': ('U298FAPT7', 'Susan Nesbitt'), 'KRRLL': ('U2B6Q2SVB', 'Corey Harrilal'), 'TNLRSN': ('U2C90DSLF', 'Dion Larson'), 'TNMRS': ('U2C90LDS9', 'Dan Morse'), 'AXTS': ('U2FCY2FBR', 'Ashu Desai'), 'ARNSNJRTN': ('U2QTVG278', 'Jordan Arnesen'), 'XSNK': ('U41MM2A1Z', 'Chase Wang'), 'ALLKRTN': ('U48LVBV34', 'Eliel Gordon'), 'TSMN': ('U4CEBV4SW', 'Mona Desai'), 'KXMMS': ('U6WMDD6U8', 'Kaichi Momose'), 'KKMMS': ('U6WMDD6U8', 'Kaichi Momose'), 'HRTTJN': ('U6WQK3Q73', 'Juan Hurtado'), 'KRSTFRTLR': ('U6WRNH1JM', 'Christopher Taylor'), 'XJF': ('U6X9KPH7C', 'Jeff Chiu'), 'ATMSNFN': ('U6X9L8VAN', 'Novan Adams'), 'ATMSTN': ('U6X9L8VAN', 'Donny Adams'), 'SNKLFS': ('U6XA0UA10', 'Yves Songolo'), 'KRSFRTNNT': ('U6XCP1NLU', 'Ferdinand Cruz'), 'KLSSM': ('U6XCTHTQQ', 'Sam Galizia'), 'HRLLM0': ('U6XDGCKFF', 'Matthew Harrilal'), 'HRLLMTF': ('U6XDGCKFF', 'Matthew Harrilal'), 'SRTN': ('U6XDKSREZ', 'Tony Cioara'), 'XRTN': ('U6XDKSREZ', 'Tony Cioara'), 'MLTNK': ('U6XDV6CVA', 'Melody Yang'), 'SKKS': ('U6XE4NNSZ', 'Sky Xu'), 'XNJN0N': ('U6XJLPQ9Y', 'Johnathan Chen'), 'XNJNTN': ('U6XJLPQ9Y', 'Johnathan Chen'), 'KRSMLTN': ('U6XRWEQGY', 'Chris Mauldin'), 'ALRKR': ('U6XV0FFEW', 'Alirie Gray'), 'AKXXN': ('U6Y6KU78W', 'Uchenna Aguocha'), 'AKKKN': ('U6Y6KU78W', 'Uchenna Aguocha'), 'TNKNMKTNLT': ('U6YCJRXGF', 'Duncan MacDonald'), 'ANSLPRJTR': ('U6YCV95L7', 'Ansel Bridgewater'), 'ANTRTSKT': ('U6YD3BYBD', 'Andrew Tsukuda'), 'JMSRSNTS': ('U6YFC7074', 'James Rezendes'), 'AMSRSNTS': ('U6YFC7074', 'James Rezendes'), 'AKNFTLR': ('U6YGZN9HD', 'Egon Fiedler'), 'PRNTLT': ('U6YHCA79U', 'Elliot Briant'), 'ASTTLLMR': ('U6YHKG1RQ', 'Elmer Astudillo'), 'ARKPRS': ('U6YMF5THV', 'Erik Perez'), 'ARKPRTS': ('U6YMF5THV', 'Erik Perez'), 'AKXSTKR': ('U6YMU9QCF', 'Aakash Sudhakar'), 'KXSTKR': ('U6YMU9QCF', 'Kash Sudhakar'), 'FLSNK': ('U6YP200VB', 'Phyllis Wong'), 'KNKX': ('U6YV4A45C', 'Tia King'), 'KNTRMR': ('U6Z4KNWCD', 'Kendra Moore'), 'JKTRN': ('U6Z5ZDKP1', 'Jake Tran'), 'AKTRN': ('U6Z5ZDKP1', 'Jake Tran'), 'FLKSMNTL': ('U6Z9LHPEH', 'Mondale Felix'), 'MXRRHN': ('U6ZCE0AKG', 'Rohan Mishra'), 'JSTNSTR': ('U703HM5PY', 'Justin Sitter'), 'ASTNSTR': ('U703HM5PY', 'Justin Sitter'), 'ANKSN': ('U72SB0WG6', 'Sunny Ouyang'), 'TPKRMKN': ('U74A620U8', 'Megan Doepker'), 'AXPMKL': ('U7U7MS551', 'Michael Ashby'), 'AXPMXL': ('U7U7MS551', 'Michael Ashby'), 'ALNTN': ('U7V12NBSR', 'Alena Dagneau'), 'ALNTKN': ('U7V12NBSR', 'Alena Dagneau'), 'ARKSNXS': ('U8M6VPKUZ', 'Erick Sanchez'), 'ARKSNKTS': ('U8M6VPKUZ', 'Erick Sanchez'), 'JRSNTS': ('U8MP28D9S', 'Joe Rezendes'), 'ARSNTS': ('U8MP28D9S', 'Joe Rezendes'), 'ASTRXN': ('U8NHWGBGW', 'Shane Austrie'), 'KLPRNL': ('U8NHWRX0W', 'Parnell Kelley'), 'ASJS': ('U8NMLKGDU', 'Jayce Azua'), 'MTSJS': ('U8X0NTGER', 'Mateusz Wijas'), 'MTXJS': ('U8X0NTGER', 'Mateusz Wijas'), 'ARTLKS': ('U90HP2ZT6', 'Lucas Arruda'), 'MKNMR': ('U916G04LB', 'Miki Nomura'), 'ARN': ('U9HT8DV8S', 'Erin'), 'TSMKN': ('U9PA0BZQW', 'Megan Dias'), 'KLTRX': ('U9W8R4A2W', 'Chloe Darsch'), 'PLKRTN': ('UBJU66HLG', 'Courtney Bell'), 'ATRNKNSLS': ('UBZLA95GV', 'Adriana Gonzalez'), 'TNRKSPR': ('UC36F4P2M', 'Dani Roxberry'), 'ANSPLTNK': ('UC45RJQ7M', 'Anne Spalding'), 'JNSKR': ('UC7PP1PTR', 'Jen Sikora'), 'ANSKR': ('UC7PP1PTR', 'Jen Sikora'), 'RNSFT': ('UCB3G0JKS', 'Rinni Swift'), 'KTK0NPL': ('UCB3PRBME', 'Nyapal Gatkuoth'), 'KTKTNPL': ('UCB3PRBME', 'Nyapal Gatkuoth'), 'ASMNMT': ('UCB58P2V6', 'Medi Assumani'), 'KRNMJX': ('UCB8SBFJ4', 'Joshua Geronimo'), 'JRNMJX': ('UCB8SBFJ4', 'Joshua Geronimo'), 'ANPL': ('UCB8T1AG0', 'Anna Pawl'), 'XKKF0': ('UCB8U00KA', 'Faith Chikwekwe'), 'XKKFT': ('UCB8U00KA', 'Faith Chikwekwe'), 'N0NPL': ('UCB8WCDTJ', 'Nathan Pillai'), 'NTNPL': ('UCB8WCDTJ', 'Nathan Pillai'), 'KPTSMKLTMF': ('UCB8Y9ZQ8', 'Timofey Makhlay Kapitsa'), 'KLPFSKRP': ('UCB8YJNBT', 'Sukhrob Golibboev'), 'KLSN': ('UCB91TXS4', 'KJ Wilson'), 'M0FRKSFNK': ('UCBC6K65P', 'Matthew Phraxayavong'), 'MTFRKSFNK': ('UCBC6K65P', 'Matthew Phraxayavong'), 'KLNSSN': ('UCBC9725P', 'Sean Glancy'), 'ANTRSNJSMN': ('UCBD9KCQH', 'Jasmine Anderson'), 'HFJKP': ('UCBDA2GGH', 'Jacob Haff'), 'KNKTM': ('UCBDBB3LZ', 'Tim Kaing'), 'KHLKNR': ('UCBDDHX7T', 'Connor Cahill'), 'TLNFN': ('UCBDPE94Z', 'Dylan Finn'), 'JFRMNTS': ('UCBHLEZEY', 'Javier Mendoza'), 'AFRMNTS': ('UCBHLEZEY', 'Javier Mendoza'), 'PRKRTNF': ('UCBHMLWEQ', 'Parker Tenove'), 'HJKSN': ('UCBHQSTB6', 'Jackson Ho'), 'PXRRK': ('UCBHS20S0', 'Eric Botcher'), 'KNMR': ('UCBHS9M3N', 'Keoni Murray'), 'NKLSF': ('UCBKC02JY', 'Nicolai Safai'), 'SRNSFT': ('UCBLQF0R1', 'Sarin Swift'), 'JMMKRR': ('UCBLQTD7V', 'Jamie McCrory'), 'AMMKRR': ('UCBLQTD7V', 'Jamie McCrory'), 'RKRTRTRKS': ('UCBMZFL4U', 'Ricardo Rodriguez'), 'PTSTRK': ('UCBP3BYTW', 'Erik Batista'), 'TRMKN': ('UCBP4M9C4', 'Drew McGowan'), 'HNJSMKSM': ('UCBP5EN5S', 'Maximo Hinojosa'), 'HNHSMKSM': ('UCBP5EN5S', 'Maximo Hinojosa'), 'LNSL': ('UCBPUT6AX', 'Wenzel Lowe'), 'LNTSL': ('UCBPUT6AX', 'Wenzel Lowe'), 'KLTTN': ('UCBQH1P6E', 'Edwin Cloud'), 'PKRJSN': ('UCBQJD3NW', 'Jaeson Booker'), 'JMSJRM': ('UCBQLD4M8', 'Jeremy James'), 'AMSJRM': ('UCBQLD4M8', 'Jeremy James'), 'ARKNKLK': ('UCBS1DSF5', 'Erica Naglik'), 'PLKLL': ('UCBS25JKD', 'Khallil Bailey'), 'KFSKNLN': ('UCBS25XMZ', 'Nolan Kovacik'), 'MRFKTR': ('UCBS37LKV', 'Victoria Murray'), 'HHLKRLK': ('UCBS4EW59', 'Luc Highwalker'), 'ALMFMKMT': ('UCBS8JUHH', 'Makhmud Islamov'), 'KLNN': ('UCBSELQ2F', 'Colleen Ni'), 'NJNKS': ('UCBSELQ2F', 'Zhanxi Ni'), 'TSRMR': ('UCC0FMXCJ', 'Dacio Romero'), 'TXRMR': ('UCC0FMXCJ', 'Dacio Romero'), 'HMPRTJSMN': ('UCC0GD5V0', 'Jasmine Humbert'), 'XRPNSTFN': ('UCC0GL52N', 'Stephanie Cherubin'), 'LSRNS': ('UCC0H4UJE', 'Lucia Reynoso'), 'LXRNS': ('UCC0H4UJE', 'Lucia Reynoso'), 'KMPLMRN': ('UCC0HC7D0', 'Marianna Campbell'), 'RMNT': ('UCC0KLBPU', 'Raymond Wu'), 'ANXJN': ('UCC37PD6D', 'Anisha Jain'), 'NKNRN': ('UCC4RHFU5', 'Ryan Nguyen'), 'JN0NKP': ('UCC4RUF4M', 'Jonathan Kopp'), 'ANTNKP': ('UCC4RUF4M', 'Jonathan Kopp'), 'XRXKM': ('UCC4S13NZ', 'Cherish Kim'), 'HRSNSML': ('UCC4SJBL5', 'Samuel Harrison'), 'KRNMRMN': ('UCC4SUSHK', 'Ramon Geronimo'), 'JRNMRMN': ('UCC4SUSHK', 'Ramon Geronimo'), 'TRKFRNTRN': ('UCC4TPF5K', 'Drake Vorndran'), 'KFRNTRN': ('UCC4TPF5K', 'Ki Vorndran'), 'PSRSLFTR': ('UCC4U4V53', 'Salvador Becerra'), 'ALXLP': ('UCCL1R3EZ', 'Ali Shalabi'), 'LTMS': ('UCCRGTD0X', 'Thomas Lee'), 'ARKSPNS': ('UCCS7HWGP', 'Erick Espinoza'), 'ARKSPNTS': ('UCCS7HWGP', 'Erick Espinoza'), 'ASPNSSL': ('UCCS7HWGP', 'Wesley Espinoza'), 'ASPNTSSL': ('UCCS7HWGP', 'Wesley Espinoza'), 'PNSKNK': ('UCCSGECPJ', 'Ikey Benzaken'), 'PNTSKNK': ('UCCSGECPJ', 'Ikey Benzaken'), 'RNSM0': ('UCCTF62ET', 'Ryan Smith'), 'RNSMT': ('UCCTF62ET', 'Ryan Smith'), 'TPFT': ('UCD1J9LDV', 'Fode Diop'), 'AKTRSMN': ('UCD1JMBMM', 'Aktar Zaman'), 'AKTRTSMN': ('UCD1JMBMM', 'Aktar Zaman'), 'PLPTS': ('UCD1JVCJ3', 'Betsy Bailey'), 'KPSJMR': ('UCD4Y1DCN', 'Jamar Gibbs'), 'JPSJMR': ('UCD4Y1DCN', 'Jamar Gibbs'), 'MRSLFNSNS': ('UCD53TKCN', 'Vincenzo Marcella'), 'FNKKNNNK': ('UCD9D1YH4', 'Kuan-Ying Fang'), 'ANKSTFN': ('UCDAE5GSJ', 'Stephen Ouyang'), 'ASMST': ('UCDAETD5L', 'Asim Zaidi'), 'PTJSSF': ('UCDAF4FV4', 'Seve Badajoz'), 'PTHSSF': ('UCDAF4FV4', 'Seve Badajoz'), 'AKRNSRX': ('UCDAJD4F8', 'Zurich Okoren'), 'AKRNTSRK': ('UCDAJD4F8', 'Zurich Okoren'), 'RSNST': ('UCDAKSB7Y', 'Ruhsane Sawut'), 'PKNSLM': ('UCDAMHRDL', 'William Bogans'), 'NTRT': ('UCDPM021J', 'Noah Woodward'), 'PNR': ('UCFCFQ7KK', 'Henry Bowe'), 'KNRSLT': ('UCFCGA3C1', 'Connor Oswold'), 'JKXMS': ('UCH838UC9', 'Jake Shams'), 'AKXMS': ('UCH838UC9', 'Jake Shams'), 'KPRSPN': ('UCHK87XEJ', 'Ebonne Cabarrus'), 'MLTTTNKN': ('UCHMQH2HE', 'Milad Toutounchian'), 'KRLNFRN': ('UCJ72FALU', 'Caroline Virani'), 'TTNTRJF': ('UCMTPELBC', "Jeff D'Andria"), 'PLFLPS': ('UCN7DEGP7', 'Bill Phillips'), 'TFSMT': ('UCPQD5NHM', 'Matt Davis'), 'KRSSTS': ('UCR0ANW5T', 'Stacey Garcia'), 'KRXSTS': ('UCR0ANW5T', 'Stacey Garcia'), 'AMNK': ('UCZQFV9BR', 'Amy Young'), 'TFRTRN': ('UD44P4YRE', 'Devery Doran'), 'JRJSR': ('UD57U4QAV', 'Sarah George'), 'KRKSR': ('UD57U4QAV', 'Sarah George'), 'LMFKRN': ('UEHTXECFN', 'Ryan Lamvik'), 'PRNMN': ('UEPUV52GL', 'Ian Birnam'), 'PRNNKN': ('UF83RJTHD', 'Brian Nguyen'), 'KLXRXRT': ('UFBTRMEBV', 'Richard Kalish'), 'KLXRKRT': ('UFBTRMEBV', 'Richard Kalish'), 'TMSFNTKRF': ('UFCF6M0TE', 'Thomas Vandegriff'), 'KMLSL': ('UFHMAU6Q3', 'Leslie Kim'), 'MRNRKF': ('UFSH2CGLW', 'Marianne Rogoff'), 'HNRXRPMN': ('UFY73CVKJ', 'Henry Shreibman'), 'PTT': ('UGK8D1R8E', 'Buay Tut'), 'TNKRK': ('UHJFRH545', 'Eric Deng'), 'MTLNMRTN': ('UHK2P9EPR', 'Madelyn Martin'), 'TRNLNK': ('UJK39Q5ME', 'Doreen Leong'), 'XRLTP': ('UJKNLUF9A', 'Charlie Taibi'), 'ALSP0SNTR': ('UJMHLRJRJ', 'Elizabeth Swander'), 'ALTSPTSNTR': ('UJMHLRJRJ', 'Elizabeth Swander'), 'AMPRJPN': ('UJS6MLZJM', 'Ben Ambrogi'), 'AMPRKPN': ('UJS6MLZJM', 'Ben Ambrogi'), 'TNLM': ('UJTDUJXU3', 'Daniel May'), 'JTNTN': ('UJU7FSE4C', 'Tania Gidney'), 'KTNTN': ('UJU7FSE4C', 'Tania Gidney'), 'TNLNTS': ('UJUJZANKD', 'Lindsey Dean'), 'LSTNPRSS': ('UK42V03K9', 'Precious Listana'), 'LSTNPRXS': ('UK42V03K9', 'Precious Listana'), 'JSLNSK': ('UK45MB3NG', 'Joe Zolnoski'), 'ATSLNSK': ('UK45MB3NG', 'Joe Zolnoski'), 'LRNSSN': ('UK6TA5V1D', 'Sean Lawrence'), 'PLKPRNMXL': ('UKACCG1J6', 'Michelle Blackburn'), 'PLKPRNMKL': ('UKACCG1J6', 'Michelle Blackburn'), 'JNSPSTKR': ('UKC6Y5MPH', 'Siebe Jan Stoker'), 'ANSPSTKR': ('UKC6Y5MPH', 'Siebe Jan Stoker'), 'MRT0MRF': ('UKMGT7BKJ', 'Meredith Murphy'), 'MRTTMRF': ('UKMGT7BKJ', 'Meredith Murphy'), 'KRNNPRKSMN': ('UKR7GN6FK', 'Simon Kronenberg'), 'ALMKPRT': ('UL8JXU0CR', 'Ellie MacBride'), 'TMNJS': ('UM1ESSU94', 'Jess Dahmen'), 'FRTRJNTRX': ('UM4KA8YGN', 'Trisha Regine Fuerte'), 'FRTRKNTRX': ('UM4KA8YGN', 'Trisha Regine Fuerte'), 'SLSRNTLF': ('UMB7Q5A1E', 'Celisse Randolph'), 'ALSTNPRTLFN': ('UMBUDNURY', 'Bradley Van Alstyne'), 'TRMM': ('UMCUQ3Q3U', 'Mo Drame'), 'KLTRNNR': ('UMCUQ56TC', 'Henry Calderon'), 'FLTSML': ('UMCUQAZ6W', 'Samuel Folledo'), 'NKNRK': ('UMCUQBYLA', 'Ricky Nguyen'), 'JNJTP': ('UMCUQDCEN', 'Genji Tapia'), 'KNJTP': ('UMCUQDCEN', 'Genji Tapia'), 'KLMS': ('UMCUQF28J', 'Kye Williams'), 'ALLMNSN': ('UMCUQJ3U2', 'Hassan El-Amin'), 'TKLS': ('UMCUQRMGS', 'Louis Dweck'), 'AJJRJ': ('UMCURA7A6', 'George Aoyagi'), 'AKKRK': ('UMCURA7A6', 'George Aoyagi'), 'JNSRS': ('UMCURC0LS', 'Jonasz Rice'), 'ANXRS': ('UMCURC0LS', 'Jonasz Rice'), 'HRLXN': ('UMCURHL9Y', 'Shaan Hurley'), 'NKNN': ('UMCURUVK4', 'Uyen Nguyen'), 'AMPRSNJLK': ('UMCUS202E', 'Anjelica Ambrosio'), 'AMPRXNJLK': ('UMCUS202E', 'Anjelica Ambrosio'), 'XSTNL': ('UMCUS3A2E', 'Stanley Chow'), 'FRNSSTSNK': ('UMCUS7998', 'Francis Tsang'), 'ANKLSMR': ('UMCUUSE6P', 'Samir Ingle'), 'TNFLJ': ('UMCUUUPM1', 'Donny Vallejo'), 'TNFH': ('UMCUUUPM1', 'Donny Vallejo'), 'RSSN': ('UMCUV3MGT', 'Zain Raza'), 'ALTKRLNSJS': ('UMCUVMK5Z', 'Jose Arellanes Aldaco'), 'ALTKRLNSHS': ('UMCUVMK5Z', 'Jose Arellanes Aldaco'), 'KSRN': ('UMCUW0DKM', 'Ryan Keys'), 'JRKFSNLSN': ('UMCUW80F5', 'Jarquevious Nelson'), 'ARKFSNLSN': ('UMCUW80F5', 'Jarquevious Nelson'), 'HNTRJRK': ('UMCUWBJ5R', 'Jeric Hunter'), 'LTLHN': ('UMCUWBK9R', 'Liya Tilahun'), 'KRSJNL': ('UMCUWDH35', 'Joanelly Cruz'), 'FRNKLNFN': ('UMCUWKRGB', 'Franklin Phan'), 'APRKSPSXN': ('UMCUWMFEF', 'Sebastian Abarca'), 'NKLKFLTLF': ('UMCUWN1SP', 'vladyslav nykoliuk'), 'LKNRK': ('UMCUWR9K5', 'Ruk Lakhani'), 'MKNPRN': ('UMCUWSAHZ', 'Megan Obryan'), 'TTNLRN': ('UMCUWSM7V', 'Lauren Dutton'), 'KM': ('UMCUWSY2F', 'Cao Mai'), 'KNTSKNPF': ('UMEPZ3JQK', 'Kaniet Oskonbaev'), 'ANSPLS': ('UMJ1BB3EV', 'Anas Bellouzi'), 'FRTRKKR': ('UMJ1BBQPK', 'Gary Frederick'), 'AKRNK': ('UMJ1BD8P3', 'Aucoeur Ngo'), 'NKLRX': ('UMJ1BNSQZ', 'Nicole Rocha'), 'NKLRK': ('UMJ1BNSQZ', 'Nicole Rocha'), 'LMPSNKTMNK': ('UMJ1C1YHX', 'Pasang Lama Tamang'), 'KPRLL': ('UMJ1C2XTK', 'Gabriel Lee'), 'FNMKS': ('UMJ1C5TPB', 'Max Finn'), 'SNK': ('UMJ1CUB97', 'Xing Ye'), 'KFNMRS': ('UMJ1CUFNV', 'Kevin Meyers'), 'TRKTRT': ('UMJ1D157B', 'Diyar Kudrat'), 'PRNTNXRSTFR': ('UMJ1D3DL1', 'Brandon Christoffer'), 'PRNTNKRSTFR': ('UMJ1D3DL1', 'Brandon Christoffer'), 'ANJLNLMT': ('UMJ1D560Z', 'Angelina Olmedo'), 'ANKLNLMT': ('UMJ1D560Z', 'Angelina Olmedo'), 'FSNTRSTN': ('UMJ1D7EV7', 'Tristan Fossan'), 'ALPRTSTLS': ('UMJ1DG4HX', 'Elbert Ostolaza'), 'AN0NPR0': ('UMPU6AU84', 'Anthony Protho'), 'ANTNPRT': ('UMPU6AU84', 'Anthony Protho'), 'HLSMNK': ('UMPU6PRFW', 'Ike Holzmann'), 'HLTSMNK': ('UMPU6PRFW', 'Ike Holzmann'), 'ALKNT': ('UMPU6QSNQ', 'Aleia Knight'), 'PKT': ('UMPU6TVDJ', 'Beck Haywood'), 'ANTRRS': ('UMPU759T6', 'Andrew Reyes'), 'JRMXMT': ('UMPU7650C', 'Jerome Schmidt'), 'ARMXMT': ('UMPU7650C', 'Jerome Schmidt'), 'KLPTRK': ('UMPU7708L', 'Patrick Kelly'), 'APRRTT': ('UMPU7QL4C', 'Rediet Abere'), 'JNMNR': ('UMPU7UG0L', 'John Miner'), 'ANMNR': ('UMPU7UG0L', 'John Miner'), 'PNSMPSN': ('UMPU813B6', 'Ben Simpson'), 'ANRNS': ('UMPU81SDA', 'Ian Rones'), 'AMRSK': ('UMPU8716G', 'Omar Sagoo'), 'PNTSPL': ('UMPU88GBW', 'Subal Pant'), 'KRSXNKLKSK': ('UMPU88U8L', 'Christian Galkowski'), 'KRSXNKLKFSK': ('UMPU88U8L', 'Christian Galkowski'), 'HRSNLK': ('UMPU8AF3N', 'Luke Harrison'), 'KLKSJRJ': ('UMPU8BCAY', 'Jorge Gallegos'), 'KLKSJRK': ('UMPU8BCAY', 'Jorge Gallegos'), 'JSKTRN': ('UMQCGRM4Y', 'Jessica Trinh'), 'ASKTRN': ('UMQCGRM4Y', 'Jessica Trinh'), 'KTNJ': ('UMQCH2AM6', 'Joey Gaitan'), 'ANTRLMS': ('UMQCH3280', 'Andre Williams'), 'KRLJTN': ('UMQCHL2N4', 'Gideon Crawley'), 'KRLKTN': ('UMQCHL2N4', 'Gideon Crawley'), 'KMLSNT': ('UMQCHSB6C', 'Sandy Camilo'), 'TNRRK': ('UMQCJ1D4Y', 'Tanner York'), 'PTNRTL': ('UMQCJA9UY', 'Padyn Riddell'), 'PRNSXRS': ('UMQCJBA00', 'Chris Barnes'), 'PRNSKRS': ('UMQCJBA00', 'Chris Barnes'), 'HLNTTLR': ('UMQCJC9QQ', 'Tyler Holland'), 'ALKSKR': ('UMQCJCMA4', 'Alex Gray'), 'PRNKLTR': ('UMQCJFDUG', 'Deer Brinkley'), 'PRJLXXT': ('UMQCJHJ72', 'Shashwat Prajjwal'), 'KMMRK': ('UMQCJJ6DN', 'Mark Kim'), 'ATRTTSF': ('UMQCNSLER', 'Tasfia Addrita'), 'AXPSTK': ('UMQCP0VA9', 'Ashab Siddiqui'), 'TNLTK': ('UMQCP2NF7', 'Daniel Duque'), 'PRTKNS': ('UMQCP40NR', 'Gonzo Birrueta'), 'ANKMRS': ('UMQCP4ZFF', 'Anika Morris'), 'TMLTR': ('UMQCP6MQV', 'Dom Holder'), 'PNLFRT': ('UMQCPF0G5', 'Ben Lafferty'), 'KRSTFRFRNSSK': ('UMQCPQ2MT', 'Christopher Francisco'), 'KXNSKKNSTNTN': ('UMQCQ9LH3', 'Konstantin Kishinsky'), 'PRNKLJPRL': ('UMQCQBM4M', 'Jibryll Brinkley'), 'SRSSF': ('UMQCQDXPX', 'Youssef Sawiris'), 'ANSTSKLRT': ('UMQCQE3AR', 'Anastasia Gallardo'), 'ANSTXKLRT': ('UMQCQE3AR', 'Anastasia Gallardo'), 'HPKNSRN': ('UMQCQGA3X', 'Ryan Hopkins'), 'HLFN': ('UMQCQJ5GV', 'Ivan Hall'), 'KNTF': ('UMQCQJZTP', 'Dahveyea Cowan'), 'ANFNTJN': ('UMQCQL9EH', 'Jon Infante'), 'KSTLXLSN': ('UMQCQQLSZ', 'ChelseaAnne Castelli'), 'KSTLKLSN': ('UMQCQQLSZ', 'ChelseaAnne Castelli'), 'JNMNTJN': ('UMQCQURKP', 'John Montejano'), 'ANMNTHN': ('UMQCQURKP', 'John Montejano'), 'LKPRKR': ('UMQCQV3C5', 'Luke Parker'), 'MHMTTFK': ('UMQCZ816H', 'Muhammad Tifak'), 'KNSTNTN': ('UMQKDDZV3', 'Constantino'), 'APXKKLKRN': ('UMRF0K90C', 'Abhishek Kulkarni'), 'HPT': ('UMRUWBHCM', 'Wyatt Happ'), 'KNTMRT': ('UMS8J6KNK', 'Kento Murata'), 'ANTRNFXKF': ('UMS8JC7RD', 'Andrey Novichkov'), 'ANTRNFKKF': ('UMS8JC7RD', 'Andrey Novichkov'), 'MRMK': ('UMS8JQ2ET', 'Mario McGee'), 'TTLNTM': ('UMS8K32K1', "Thom d'Olanie"), 'KRSXNLNPRKR': ('UMS8KA2J3', 'Christian Lenberger'), 'KRSXNLNPRJR': ('UMS8KA2J3', 'Christian Lenberger'), 'APTLNR': ('UMS8KFR63', 'Abdullah Noori'), 'XTKLM': ('UMS8KNNR5', 'William Chadwick'), 'PKFRN': ('UMS8KPZFZ', 'Farhan Begg'), 'ATRSPLTS': ('UMS8KSC6T', 'Audaris Blades'), 'ALKSPRKSTL': ('UMS8KSZ2T', 'Alex Barksdale'), 'APTKPS': ('UMS8KTKSB', 'Kabsa Abdi'), 'KRNSNK': ('UMSHX8W0N', 'Nick Kearns'), 'FRTSTR': ('UMSHXC0G6', 'Fritz Heider'), 'ARFNSFPR': ('UMSHXES6S', 'Arvin Seifipour'), 'ANKXNNN': ('UMSHXH0BG', 'Nyein Chan Aung'), 'ANKKNNN': ('UMSHXH0BG', 'Nyein Chan Aung'), 'ANKNNJ': ('UMSHXH0BG', 'Ninja Aung'), 'JKKTSR': ('UMSHXSVML', 'Jack Katzer'), 'AKKTSR': ('UMSHXSVML', 'Jack Katzer'), 'JSNMK': ('UMSHY8D8W', 'Jason McGee'), 'ASNMK': ('UMSHY8D8W', 'Jason McGee'), 'TFTFNS': ('UMSHYFHE2', 'David Evans'), 'PLPRKR': ('UMSHYM1GW', 'Parker Paisley'), 'ARNFNS': ('UMSHYP0VC', 'Ariane Evans'), 'ALNNKX': ('UMSHYS4BG', 'Alanna Noguchi'), 'ALNNKK': ('UMSHYS4BG', 'Alanna Noguchi'), 'ALNMSK': ('UMSHZAUQN', 'Elaine Music'), 'XT': ('UMSHZETAA', 'Chudier'), 'XTR': ('UMSHZETAA', 'Chudier'), 'MRKFM': ('UMTQS1139', 'Mark Pham'), 'APTLFXH': ('UMUNA710V', 'Shoha Abdullaev'), 'FRTFRNK': ('UMUU7JCJG', 'Veronica Fruiht'), 'PRKK0RN': ('UMVCJFA3S', 'Catherine Borg'), 'PRKKTRN': ('UMVCJFA3S', 'Catherine Borg'), 'ALTRMNNM': ('UMW6HJV1N', 'Naomi Alterman'), 'LSTRN': ('UN3F9JLKW', 'Lisa Tran'), 'TFTLPL': ('UNXF45NDS', 'David Elbel'), 'PNKNFS': ('UPSUK4E8H', 'Bianca Nieves'), 'LRNMSL': ('UQ0S08A00', 'Lauren Massell'), 'FRTJNTMKS': ('UQ8336Q8K', 'Max Fritzhand')
}])'''

app = Flask(__name__)    

@app.route('/')
def index():
    """Return homepage, AKA wake up Heroku"""
    return render_template('index.html')

@app.route('/api/', methods=['GET'])
def store_show_item():
    """Request the API to find the username and then use the slack API to send the user a message."""

    name = request.args.get('name')
    addy = request.args.get('addy')

    #name = scanned_name
    print (f'name: {name} \naddy: {addy}')

    #test name 
    #name = "Mr. Tápia Genji"

    #lowercase
    name = name.lower() #doens't seem to be needed

    #remove accented letters
    name = unidecode(name)

    #remove honorifics?
    # this will work, but it removes everything before a period, not strictly honorifics
    regex = r"\w+\. *(?=\w+)|,[\s\w]*$"
    subst = ""
    name = re.sub(regex, subst, name, 0)

    #expand common english name abbreviations
    # https://en.wiktionary.org/wiki/Appendix:Abbreviations_for_English_given_names

    #sort alphabetically
    sort_name = name.split()
    sort_name.sort()
    name = ' '.join(sort_name)

    #double metaphone conversion
    nameTuple = doublemetaphone(name)

    #debug show db
    #print (slack_db) #lol

    #debug show results
    print (f'passed in {request.args.get("name")} filtered into {name}')
    print (f'metaphone tuple: {nameTuple}')

    #check various metaphone tuple matches for name in database, return uID or error
    uID = None
    if slack_db.find_one({nameTuple[0]:{'$exists': True}}):
        uID = slack_db.find_one({nameTuple[0]:{'$exists': True}})[nameTuple[0]]
    if uID == None and nameTuple[1] is not '':
        print("Name not found, trying 2nd tuple")
        if slack_db.find_one({nameTuple[1]:{'$exists': True}}):
            uID = slack_db.find_one({nameTuple[1]:{'$exists': True}})[nameTuple[1]]

    #if uID found, send slack message.
    r_response = None
    if uID == None:
        print("ERROR: Name not found")
        #return the original passed in string so errors can be looked for
        name = request.args.get("name")
        r_response = {"success": False, "error":"name not found", "slackID":None, "name":name, "note":None}
    else: 
        print (f'FOUND: entry {uID}')
        #http url request to the slack API
        #load_dotenv() #not used over heroku
        token = os.environ.get("BOT_USER_OAUTH_ACCESS_TOKEN")
        channel = '@' + uID[0]
        #if addy 
        if addy != None:
            text = f"You've got snail mail at {addy} :love_letter:"
        else:
            text = "You've got snail mail :love_letter:"
            
        pload = {'token':token,'channel':channel,'text':text}
        r = requests.post('https://slack.com/api/chat.postMessage',data = pload)
        r_dictionary= r.json()
        #possible return that message sent successfully through the api
        error = r_dictionary.get('error') 
        r_response = {"success": r_dictionary['ok'], "error": error, "slackID":uID[0], "name":uID[1], "note":None}
        #print (r_dictionary['ok'])
        #print (r_dictionary) #debug the full api return'''

    return jsonify(r_response)
    #return redirect(url_for('index'))

if app.name == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))