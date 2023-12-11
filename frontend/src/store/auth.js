import { create } from 'zustand';
import { mountStoreDevtool } from 'simple-zustand-devtools';
import Cookies from 'js-cookie';
const useAuthStore = create((set, get) => ({
    allUserData: null, // Use this to store all user data
    loading: false,
    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username || null,
        token: Cookies.get('access_token') || null,
    }),
    setUser: (user) => set({ allUserData: user }),
    setLoading: (loading) => set({ loading }),
    isLoggedIn: () => get().allUserData !== null,
}));

if (import.meta.env && import.meta.env.DEV) {
    mountStoreDevtool('Store', useAuthStore);
  }
  //if (import.meta.env.DEV) {
 //   mountStoreDevtool('Store', useAuthStore);
//}
  

export { useAuthStore };