from flask import Flask, url_for, render_template
import sqlite3
import datetime as dt

app = Flask(__name__)
app.debug=True

@app.route('/')
def index():

    def buildRow(dfList):

        def buildCell(name,result):
            col = "red" if result in ["None", "False"] else "#C4D79B" 
            label = "&nbsp;" if result in ["None", "False", "0.0"] else result
            try:
                strRes=float(result)
            except:
                pass
            else:
                label="&nbsp;" if strRes < 0.01 else result

            return f"<table><tr><td>{name}</td><td>&nbsp;</td></tr>\n<tr><td bgcolor='{col}'>{label}</td><td>&nbsp;</td></tr></table>\n"


        #split the list of lists into 2 lists
        #iName = [x[0] for x in dfList]
        #iRes = [x[2] for x in dfList]
        newstr=""
        cellcount=0
        for item in dfList:
            newstr+=("<td><center>")
            name=item[0]
            res=item[2]
            newstr+=buildCell(name,res)
            if cellcount==10:
                newstr+=("</tr><tr>")
                cellcount=0
            cellcount+=1   
            newstr+=("<center></td>") 
        newstr+=("</tr>\n")
        return newstr 

    today=dt.datetime.today()
    thistime=today.strftime("%Y-%m-%d %H:%M")

    #connect db
    connection=sqlite3.connect('././databases/ping.db')
    cursor = connection.cursor()
    #fetch the hierachy levels
    cursor.execute(f"select * from hierarchy")
    levels=[item for item in cursor.fetchall()]

    #process start table

    htmlstr=""
    for level in levels:
        #title
        htmlstr+=(f"<h2>{level[1]}</h2>\n")
        #create new table
        htmlstr+=("<table>\n\n")
        #for this level fetch devices
        cursor.execute(f"""
        select devices.name,devices.level, current.res from Devices
            inner join current on devices.id=current.id
	        where devices.level='{level[0]}'
        """)
        devices=[device for device in cursor.fetchall()]
        #build rows(s) for this level
        htmlstr+=buildRow(devices)
        #end table
        htmlstr+=("</table>\n\n")

    return render_template('index.html', htmlstr=htmlstr, thistime=thistime)
    


if __name__ == '__main__':
    app.run("10.77.32.8",80)    