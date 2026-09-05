import { createContext ,useContext ,useReducer,useEffect,useState } from "react";
import {authApis,endpoints} from "./Apis";
import MyUserReducer from "../reducers/reducers";


export const MyUserContext = createContext();


export const UserProvider = ({children}) => {
    const [user, dispatch] = useReducer(MyUserReducer,null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadUser = async () => {
            const token = localStorage.getItem("token");
            if (!token) {
                setLoading(false);
                return;
            }
            try {
                const res = await authApis(token).get(endpoints["current-user"]);
                dispatch({
                    type: "login",
                    payload: res.data
                });
            } catch (ex) {
                console.error(ex);
                localStorage.removeItem("token");
                dispatch({
                    type: "logout"
                });
            } finally {
                setLoading(false);
            }
        };
        loadUser();
    }, []);

    return (
        <MyUserContext.Provider value={{ user, dispatch, loading }}>
            {children}
        </MyUserContext.Provider>
    );
};


export const useUser = () => {
    return useContext(MyUserContext);
};