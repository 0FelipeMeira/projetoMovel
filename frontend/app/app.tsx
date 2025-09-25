import { createStackNavigator } from "@react-navigation/stack";
import LoginScreen from "./login";
import RegisterScreen from "./register";

const Stack = createStackNavigator();

const App = () => {
  const options = {
    headerShown: false,
  };

  return (
    <Stack.Navigator screenOptions={options}>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
    </Stack.Navigator>
  );
};

export default App;
