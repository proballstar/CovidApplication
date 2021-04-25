// 2021-04-29T16:45:00.000-07:00

var data = null;

function c(arg) {
  console.log(arg)
}

$(document).ready(async function() {
  data = (await fetchData()).data;
  c('in doucument ready' + data)
});

$("#search").click(async function() {
  $("#data").removeClass("d-none")

  if($("#city").val() == "" || $("#state").val() == "Select a state") {
    $("#data").html("It looks like you're missing some information. Please make sure you've selected a city and state and try again.");
    return;
  }

  //console.log('In search' + 'city:' +  ${"#city"} + 'data:' + ${"#data"})
  await search( $("#city").val(), $("#state").val() )
});

async function search(city, state) {
  const _provider = await getProviders(city, state)
  await displayData(_provider)
}

async function fetchData() {
  return await axios.get('https://www.vaccinespotter.org/api/v0/states/CA.json')
  //return await axios.get('https://senoe.wtf/a/fakedata.json')
}

async function getProviders(city, state) {
  console.log(`${city}, ${state}`)

  let _features = window.data.features
  var _providers = []
  for(let i = 0; i < _features.length; i++) {
    if(_features[i].properties.name.toUpperCase() == city.toUpperCase() && _features[i].properties.state.toUpperCase() == state.toUpperCase() && _features[i].properties.appointments_available) {
      _providers.push(_features[i])

      /*c('city' + city)
      c('state'+ state)
      c('appointments' + _features[i].properties.appointments_available)

      console.log("a")*/
    }
  }
  /*
  c('in getProviders')
  c('features' + _features)
  c('_providers'+ _providers)*/

  console.log(_providers)

  return _providers
}

async function displayData(_provider) {
  console.log(_provider);

  let _data = _provider;
  let _html = "";

  for(let i = 0; i < _data.length; i++) {
    let _prop = _data[i].properties

    _html += `
    <div class="card">
      <h3 class="fw-500 m-0">${_prop.provider_brand_name}</h3>
      <a href="${_prop.url}">${_prop.url}</a>
      <hr>`;
    
    // loop through all appointments    
    for (let i = 0; i < _prop.appointments.length; i++) {
      let time = new Date(_prop.appointments[i].time);
      time = time.toLocaleString();

      _html += `
      <p>
      Time: ${time}
      <br>
      Dose: ${_prop.appointments[i].type}
      </p>
      `
    }

    _html += `
      <p>
      ${_prop.address}
      <br>
      ${_prop.city}, ${_prop.postal_code}
      </p>
    </div>
    `;
  }

  if(_data.length == 0) {
    _html = "<p>Sorry, no vaccines are available</p>"
  }

  $("#data").html(_html);
}