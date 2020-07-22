var minAmountToRedeem = 20;
var autoRedeemAmount;
var userTotal = 12;

var yesterday = (function(d){ d.setDate(d.getDate()-1); return d})(new Date);

var historyData = [ { amount : 20.10, date : null },
                    { amount : 25.20, date : yesterday },
                    { amount : 23.50, date : new Date(2019, 2, 13) }];

function loadProgress()
{
  var c = document.getElementById("canvas");
  if (c != null)
  {
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(150, 150, 120, 0, 2 * Math.PI);
    ctx.lineWidth = 40;
    ctx.strokeStyle = "#d5d3d2";
    ctx.stroke();

    var startPI = 3 * Math.PI / 2
    ctx.beginPath();
    ctx.arc(150, 150, 120, startPI, (2 * Math.PI * (userTotal / minAmountToRedeem)) + startPI);
    ctx.lineWidth = 40;
    ctx.strokeStyle = "#830065";
    ctx.stroke();
    console.log(userTotal / minAmountToRedeem);
  }
}

function showDialog()
{
  var c = document.getElementById("dialog-background");
  c.style.display = "block";
}

function hideDialog()
{
  var c = document.getElementById("dialog-background");
  c.style.display = "none";
}

function dashboardSetup()
{
  loadProgress();
  //setFraction();
}

function setFraction()
{
  document.getElementById("fraction").innerHTML = "$" + userTotal + "/" + minAmountToRedeem;
}

function loadHistory()
{
  var table = document.getElementById("settings-table");
  for (var i = 0; i < historyData.length; ++i)
  {
    let newRow = table.insertRow(-1);
    let cellAmount = newRow.insertCell(0);
    cellAmount.appendChild(createPAmount(historyData[i].amount));
    let cellDate = newRow.insertCell(1);
    cellDate.appendChild(createPDate(historyData[i].date));
    console.log(historyData[i].amount + ": " + historyData[i].date);
  }
}

function createPAmount(text)
{
  var tdP = document.createElement("p");
  tdP.classList.add("history-amount");
  tdP.innerHTML = "$" + text.toFixed(2);
  return tdP;
}

function createPDate(date)
{
  var tdP = document.createElement("p");
  tdP.classList.add("history-date");
  if (date === null)
    tdP.innerHTML = "Pending";
  else if (date === yesterday)
    tdP.innerHTML = "Yesterday";
  else
    tdP.innerHTML = (date.getMonth()+1) + '/' + date.getDate() + '/' +  date.getFullYear();
  return tdP;
}
