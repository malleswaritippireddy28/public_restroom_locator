document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([11.0168, 76.9558], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    var routingControl = L.Routing.control({
        waypoints: [
            L.latLng(11.0168, 76.9558),
            L.latLng(11.0055, 76.9665),
        ],
    }).addTo(map);

    var locations = [
        {
            coordinates: [11.0164, 76.9681],
            name: 'Location 2',
            rating: 4.5,
            reviews: ['Great place!', 'Clean facilities.'],
        },
        {
            coordinates: [10.9914, 76.9660],
            name: 'Location 3',
            rating: 3.8,
            reviews: ['Good service.', 'Could be cleaner.'],
        },
        {
            coordinates: [11.0249, 77.0315],
            name: 'Location 4',
            rating: 4.2,
            reviews: ['Nice atmosphere.', 'Friendly staff.'],
        },
        {
            coordinates: [11.0097, 76.9539],
            name: 'Location 5',
            rating: 4.7,
            reviews: ['Excellent!', 'Very well-maintained.'],
        },
    ];

    var feedbackForm = document.getElementById('feedbackForm');
    var feedbackDisplay = document.getElementById('feedbackDisplay');
    var submitFeedbackButton = document.getElementById('submitFeedback');
    var feedbackText = document.getElementById('feedbackText');
    var washroomSelection = document.getElementById('washroomSelection');
    var washroomDisplaySelection = document.getElementById('washroomDisplaySelection');
    var feedbackList = document.getElementById('feedbackList');
    var giveFeedbackButton = document.getElementById('giveFeedback');
    var readFeedbackButton = document.getElementById('readFeedback');

    giveFeedbackButton.addEventListener('click', function () {
        feedbackForm.style.display = 'block';
        feedbackDisplay.style.display = 'none';
    });

    readFeedbackButton.addEventListener('click', function () {
        feedbackForm.style.display = 'none';
        feedbackDisplay.style.display = 'block';
    });

    submitFeedbackButton.addEventListener('click', function () {
        // Send feedback to the server
        var selectedWashroom = washroomSelection.value;
        var userFeedback = feedbackText.value;

        // Here, you should send the feedback data to the server for storage

        // Clear the form
        feedbackText.value = '';
        washroomSelection.value = 'Location 2';
    });

    washroomDisplaySelection.addEventListener('change', function () {
        // Get and display feedback for the selected washroom
        var selectedWashroom = washroomDisplaySelection.value;
        var feedbackData = getFeedbackData(selectedWashroom);

        feedbackList.innerHTML = feedbackData.join('<br>');
    });

    function getFeedbackData(washroom) {
        // Simulated function to fetch feedback data for the selected washroom
        return [
            'Feedback 1 for ' + washroom,
            'Feedback 2 for ' + washroom,
            'Feedback 3 for ' + washroom,
        ];
    }

    // Get user's location
    map.locate({ setView: true, maxZoom: 14 });

    map.on('locationfound', function (e) {
        routingControl.setWaypoints([
            L.latLng(e.latlng),
            routingControl.getWaypoints()[1].latLng,
        ]);
    });
});
