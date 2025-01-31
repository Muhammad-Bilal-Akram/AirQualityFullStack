import NavBar from "./components/NavBar";
import CurrentAirQualityIndicator from "./components/CurrentAirQualityIndicator";
import AverageAirQuality from "./components/AverageAirQuality";
import MapComponent from "./components/MapComponent";

function App() {
  return (
    <div className="App">
      <NavBar />
      <CurrentAirQualityIndicator />
      <AverageAirQuality />
      <MapComponent />
    </div>
  );
}

export default App;
