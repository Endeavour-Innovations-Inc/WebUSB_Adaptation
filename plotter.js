//****************************** csv file handling ******************************//
//declare two arrays to store time and sine values

const time_data = []; //global time variable
const point_data = []; //global data variable

initiateProgram();

function initiateProgram() {
    // Event listener for file input
    document.getElementById('uploadfile').addEventListener('change', function(event){
        const file = event.target.files[0];
        parseCSV(file);
    });

    //resets canvas
    document.getElementById('reset').addEventListener('click', () => {
        time_data.length = 0; //global time variable
        point_data.length = 0; //global data variable
        makePlotly(time_data, point_data);
    });

    makePlotly(time_data, point_data); // Initial call to create an empty plot
}

function parseCSV(file) {
    Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            time_data.length = 0;     //clear out time array
            point_data.length = 0;    //clear out data_point array

            for(let i = 0; i < results.data.length; i++) {
                time_data.push(results.data[i].t);      //push time values into time_data[]
                point_data.push(results.data[i].data);  //push point values into point_data[]
            }
            makePlotly(time_data, point_data);
        }
    });
}

//****************************** Plotly.js Graph Control ******************************//
//data graphing control
function makePlotly(time_data, point_data) {
    const myChart = document.getElementById('chart');
    Plotly.newPlot(myChart, data, layout, config);
}

//automatically resize to fit device's window size
var config = {responsive: true}

//first data trace 
var trace1 = {
    x: time_data,   //x-axis data
    y: point_data,  //y-axis datas
    type:'line'     //chart type
}

//data to be plotted to chart (for future plotting multiple data on the same graph)
var data = [trace1];

//plotly chart customization
var layout = {
    autosize: true,
    title:{
      text: 'Input Signal', //chart title
      font:{
        family: 'Arial',    //title's font type
        size: 25            //title's font size
      }
    },

    xaxis:{
      title:{
        text: 'Time', //chart title
        font:{
          family: 'Arial',    //title's font type
          size: 20            //title's font size
        }
      }
    },

    yaxis:{
      title:{
        text: 'Amplitude (V)', //chart title
        font:{
          family: 'Arial',    //title's font type
          size: 20            //title's font size
        }
      }
    },
};

function exportToExcel() {
  // Convert time_data and point_data into an array of objects
  let rows = [];
  for (let i = 0; i < time_data.length; i++) {
      rows.push({t: time_data[i], data: point_data[i]});
  }

  let ws = XLSX.utils.json_to_sheet(rows); // Convert the rows to worksheet format
  let wb = XLSX.utils.book_new(); // Create a new workbook
  XLSX.utils.book_append_sheet(wb, ws, "Data"); // Append the worksheet to the workbook
  XLSX.writeFile(wb, "data.csv"); // Save the workbook as an Excel file
}


// Assuming the export button has been added to your HTML with the ID "export"
document.getElementById('export').addEventListener('click', exportToExcel);
