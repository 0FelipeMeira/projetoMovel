import { createStackNavigator } from "@react-navigation/stack";
import AddScreen from "./add";
import EditScreen from "./edit";
import HomeScreen from "./home";
import LoginScreen from "./login";
import RegisterScreen from "./register";
import AlarmScreen from "./alarm";

const Stack = createStackNavigator();

const App = () => {
  const options = {
    headerShown: false,
  };

  return (
    <Stack.Navigator screenOptions={options}>
      <Stack.Screen name="Alarm" component={AlarmScreen} />
      <Stack.Screen name="Add" component={AddScreen} />
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Edit" component={EditScreen} />
    </Stack.Navigator>
  );
};

export default App;
