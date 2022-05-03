from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)

getCounterUrl = "https://getcounterval.azurewebsites.net/api/getcounterval?name={0}"
updateCounterUrl = "https://updatecounterval.azurewebsites.net/api/updatecounter?name={0}&value={1}"
c1Val, c2Val = None, None
first_request = True


def getCounter1():
    rqst = requests.get(
        getCounterUrl.format("Counter1"))
    return int(rqst.content)


def getCounter2():
    rqst = requests.get(
        getCounterUrl.format("Counter2"))
    return int(rqst.content)


def getCounters():
    global c1Val, c2Val
    c1Val = getCounter1()
    c2Val = getCounter2()


@app.route("/")
def index():
    if(first_request):
        getCounters()
    return render_template("index.html", counter1=c1Val, counter2=c2Val)


def incCounter(counter, currVal):
    global first_request, c1Val, c2Val
    res = requests.get(updateCounterUrl.format(counter, currVal + 1))
    if(counter == "Counter1"):
        c1Val += 1
    else:
        c2Val += 1
    first_request = False
    return redirect(url_for('index'))


@app.route("/incCounter1")
def incCounter1():
    getCounters()
    return incCounter("Counter1", c1Val)


@app.route("/incCounter2")
def incCounter2():
    getCounters()
    return incCounter("Counter2", c2Val)


if __name__ == "__main__":
    app.run(debug=True)
