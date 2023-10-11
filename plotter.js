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
