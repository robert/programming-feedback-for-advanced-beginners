// Array of object markers
const markers = [
  {
    coords: { lat: 37.7638, lng: -122.469 },
    content:
      "<h3>San Tung</h3><p>Chinese restaurant with delicious dry fried chicken wings.</p><a href='https://goo.gl/maps/wiqva8qzW9bBoJRJ6' target='_blank'>Get directions</a>",
    category: "eat"
  },
  {
    coords: { lat: 37.7332, lng: -122.4344 },
    content:
      "<h3>One Wan Thai Restaurant</h3><p>Vast selection of delicious Thai curries, noodles, and soups with beautiful plating.</p><a href='https://goo.gl/maps/zCosF1XA5d2Mf1ReA' target='_blank'>Get directions</a> ",
    category: "eat"
  },
  {
    coords: { lat: 37.7819, lng: -122.4101 },
    content:
      "<h3>Tu Lan</h3><p>Hole-in-the-wall Vietnamese restaurant with the best beef salad.</p><a href='https://goo.gl/maps/aNMsAqpzZ9wzeaW89' target='_blank'>Get directions</a> ",
    category: "eat"
  },
  {
    coords: { lat: 37.7639, lng: -122.4673 },
    content:
      "<h3>Manna</h3><p>Hole-in-the-wall family-owned Korean restaurant with the best tofu soup.</p><a href='https://goo.gl/maps/TkAFCrGrswH76hmT8' target='_blank'>Get directions</a> ",
    category: "eat"
  },
  {
    coords: { lat: 37.8015, lng: -122.3975 },
    content:
      "<h3>Exploratorium</h3><p>Hands on science museum for all ages.</p><a href='https://goo.gl/maps/GhdjWJTFFnW6tUZB8' target='_blank'>Get directions</a>",
    category: "play"
  },
  {
    coords: { lat: 37.7699, lng: -122.4661 },
    content:
      "<h3>California Academy of Sciences</h3><p>Four-story science museum with rooftop garden in Golden Gate Park.</p><a href='https://goo.gl/maps/fYWNUDFHFaFsmBYs9' target='_blank'>Get directions</a>",
    category: "play"
  },
  {
    coords: { lat: 37.761, lng: -122.4126 },
    content:
      "<h3>Mission Cliffs</h3><p>Climbing gym with top-roping, bouldering, and fitness classes.</p><a href='https://goo.gl/maps/FiesP46PyEahaVxN6' target='_blank'>Get directions</a>",
    category: "play"
  },
  {
    coords: { lat: 37.7754, lng: -122.4377 },
    content:
      "<h3>Emporium</h3><p>Lively barcade with arcade games, pool, and air hockey.</p><a href='https://goo.gl/maps/aAFSMgJmVg3Lm8SJA' target='_blank'>Get directions</a>",
    category: "play"
  },
  {
    coords: { lat: 37.7399, lng: -122.4091 },
    content:
      "<h3>Bare Bottle</h3><p>Spacious brewery with wide selection of beers on tap, acrcade games, and rotating food trucks.</p><a href='https://goo.gl/maps/PmB4NdxAvxTkJohh6' target='_blank'>Get directions</a>",
    category: "drink"
  },
  {
    coords: { lat: 37.728263, lng: -122.404139 },
    content:
      "<h3>Fermet, Drink, Repeat</h3><p>Small brewery with a few beers and kombuchas on tap, board games, and bring your own food.</p><a href='https://goo.gl/maps/JG2skPodDpMS3y7y7' target='_blank'>Get directions</a>",
    category: "drink"
  },
  {
    coords: { lat: 37.757761, lng: -122.388084 },
    content:
      "<h3>Magnolia Brewing</h3><p>Spacious brewery with many IPAs on tap and snacks.</p><a href='https://goo.gl/maps/FGYYSRVHWDxr2oKp6' target='_blank'>Get directions</a>",
    category: "drink"
  },
  {
    coords: { lat: 37.784, lng: -122.4091 },
    content:
      "<h3>Mikkeller Bar</h3><p>Spacious gastropub with wide beer selection in downtown SF.</p><a href='https://goo.gl/maps/H2RR8ZA6PFPjb44EA' target='_blank'>Get directions</a>",
    category: "drink"
  }
];

// Init gooMarkers to be able to use map setVisible property
let gooMarkers = [];
let infoWindowsList = [];

function initMap() {
  // Map options, setting SF to center
  let options = {
    zoom: 12,
    center: { lat: 37.7749, lng: -122.4194 }
  };
  // New map
  let map = new google.maps.Map(document.getElementById("map"), options);

  // Add all markers
  for (let i = 0; i < markers.length; i++) {
    addMarker(markers[i]);
  }

  // Add Marker Function
  function addMarker(props) {
    let marker = new google.maps.Marker({
      position: props.coords,
      map: map,
      category: props.category,
      content: props.content
    });

    gooMarkers.push(marker);

    // Add marker content
    let infoWindow = new google.maps.InfoWindow({
      content: props.content
    });
    marker.addListener("click", function() {
      infoWindow.open(map, marker);
      infoWindowsList.push(infoWindow);
    });

    // Close all info windows on map click
    google.maps.event.addListener(map, "click", function() {
      infoWindow.close();
    });
  }
}

// Filter function when button is clicked
let filterFunc = function(category) {
  // Returns the category clicked
  for (i = 0; i < gooMarkers.length; i++) {
    if (gooMarkers[i].category === category || category === "reset") {
      gooMarkers[i].setVisible(true);
    } else {
      gooMarkers[i].setVisible(false);
    }
  }

  // Closes all infowindows
  for (i = 0; i < infoWindowsList.length; i++) {
    infoWindowsList[i].close();
  }

  // Highlights selected button with active class
  const parentButton = document.getElementById("myDiv");
  // for loop through all buttons to reset style
  for (let i = 0; i < parentButton.children.length; i++) {
    parentButton.children[i].classList.remove("active");
  }
  document.getElementById(category).classList.add("active");
};
