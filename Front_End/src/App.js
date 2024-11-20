import { Routes, Route} from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Manipulate from './pages/Manipulate';
import Insert from './pages/Insert';
import Query from './pages/Query';
import AdvQuery from './pages/AdvQuery';


function App() {

  return (
    //Routers to pages
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/login' element={<Login />} />
      <Route path='/register' element={<Register />} />
      <Route path='/manipulate' element={<Manipulate />} />
      <Route path='/insert' element={<Insert />} /> 
      <Route path='/query' element={<Query />} />
      <Route path='/advQuery' element={<AdvQuery />} />
    </Routes>
  );
}

export default App;