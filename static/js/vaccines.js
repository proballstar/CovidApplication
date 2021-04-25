// 2021-04-29T16:45:00.000-07:00

var data = null;

$("#search").click(async function() {
  $("#data").removeClass("d-none");

  if($("#city").val() == "" || $("#state").val() == "Select a state") {
    $("#data").html("It looks like you're missing some information. Please make sure you've selected a city and state and try again.");
    return;
  }

  if(data == null) {
    data = (await fetchData($("#state").val())).data;
  }

  //console.log('In search' + 'city:' +  ${"#city"} + 'data:' + ${"#data"})
  await search( $("#city").val(), $("#state").val() );
});

async function search(city, state) {
  const _provider = await getProviders(city, state);
  await displayData(_provider);
}

async function fetchData(state) {
  /*
  vaccinespotter.org: actual api
  senoe.wtf: test api
  */
  return await axios.get(`https://www.vaccinespotter.org/api/v0/states/${state}.json`)
  //return await axios.get('https://senoe.wtf/a/fakedata.json'); 
}

async function getProviders(city, state) {
  console.log(`${city}, ${state}`);

  let _features = window.data.features;
  var _providers = [];
  for(let i = 0; i < _features.length; i++) {
    if(_features[i].properties.name.toLowerCase() == city.toLowerCase() && _features[i].properties.state.toLowerCase() == state.toLowerCase()) {
      _providers.push(_features[i]);
    }
  }

  console.log(_providers);

  return _providers;
}

async function displayData(_provider) {
  console.log(_provider);

  let _data = _provider;
  let _html = "";

  for(let i = 0; i < _data.length; i++) {
    let _prop = _data[i].properties;

    _html += `
    <div class="card">
      <h3 class="fw-500 m-0">${_prop.provider_brand_name}</h3>
      <a href="${_prop.url}">${_prop.url}</a>
      <br>
      <span>Appointments Available: ${_prop.appointments_available}</span>
      <hr>`;
    
    for (let i = 0; i < _prop.appointments.length; i++) {
      let time = new Date(_prop.appointments[i].time);
      time = time.toLocaleString();

      _html += `
      <p>
      Time: ${time}
      <br>
      Dose: ${_prop.appointments[i].type}
      </p>
      `;
    }

    _html += `
      <hr>
      <p>
      ${_prop.address}
      <br>
      ${_prop.city}, ${_prop.postal_code}
      </p>
    </div>
    `;
  }

  if(_data.length == 0) {
    _html = "<p>Sorry, no vaccines are currently available for the selected city at this time.</p>";
  }

  $("#data").html(_html);
}