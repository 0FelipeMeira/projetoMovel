import { createStackNavigator } from "@react-navigation/stack";
import LoginScreen from "./login";
import RegisterScreen from "./register";
import HomeScreen from "./home";
import EditScreen from "./edit";

const Stack = createStackNavigator();

const App = () => {
  const options = {
    headerShown: false,
  };

  return (
    <Stack.Navigator screenOptions={options}>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Edit" component={EditScreen} />
    </Stack.Navigator>
  );
};

export default App;
