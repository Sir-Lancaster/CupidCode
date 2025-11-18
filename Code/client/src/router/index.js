import { createRouter, createWebHashHistory } from 'vue-router'
import { makeRequest } from '../utils/make_request'
// General
import Login from '../components/Login.vue'
import Welcome from '../components/Welcome.vue'
import SignUp from '../components/SignUp.vue'
import NotFound from '../components/NotFound.vue'
import DaterHome from '../DaterVues/DaterHome.vue'
import CupidHome from '../CupidVues/CupidHome.vue'
import ManagerHome from '../ManagerVues/ManagerHome.vue'
import Suspended from '../components/Suspended.vue'

// Dater specific
import AiChat from '../DaterVues/AiChat.vue'
import AiListen from '../DaterVues/AiListen.vue'
import CupidCash from '../DaterVues/CupidCash.vue'
import DaterProfile from '../DaterVues/DaterProfile.vue'
import DaterFeedback from '../DaterVues/DaterFeedback.vue'
import DaterGigs from '../DaterVues/DaterGigs.vue'
import Calendar from '../DaterVues/Calendar.vue'

// Cupid Specific
import CupidDetails from '../CupidVues/CupidDetails.vue'
import CupidFeedback from '../CupidVues/CupidFeedback.vue'
import GigDetails from '../CupidVues/GigDetails.vue'
import GigComplete from '../CupidVues/GigComplete.vue'

// Manager Specific
import Cupid from '../ManagerVues/Cupid.vue'
import Daters from '../ManagerVues/Daters.vue'
import CreateGig from '../DaterVues/CreateGig.vue';

const routes = [
    {
        path: '/',
        name: 'Login',
        component: Login
    },
    // {
    //     path: '/login',
    //     name: 'Login',
    //     component: Login
    // },
    {
        path: '/register',
        name: 'Register',
        component: SignUp
    },
    {
        path: '/suspended',
        name: 'SuspendHome',
        component: Suspended
    },
    {
        path: '/dater/home/:id',
        name: 'DaterHome',
        component: DaterHome,
    },
    {
        path: '/dater/chat/:id',
        name: 'AiChat',
        component: AiChat
    },
    {
        path: '/dater/listen/:id',
        name: 'AiListen',
        component: AiListen
    },
    {
        path: '/dater/balance/:id',
        name: 'CupidCash',
        component: CupidCash
    },
    {
        path: '/dater/profile/:id',
        name: 'DaterProfile',
        component: DaterProfile
    },
    {
        path: '/dater/gigs/:id',
        name: 'DaterGigs',
        component: DaterGigs,
    },
    {
        path: '/dater/feedback/:id',
        name: 'DaterFeedback',
        component: DaterFeedback
    },
    {
        path: '/dater/CreateGig/:id',
        name: 'CreateGig',
        component: CreateGig
    },
    
    {
        path: '/dater/calendar/:id',
        name: 'Calendar',
        component: Calendar
    },

    {
        path: '/cupid/home/:id',
        name: 'CupidHome',
        component: CupidHome,
    },
    {
        path: '/cupid/gig/:id',
        name: 'GigDetails',
        component: GigDetails,
    },
    {
        path: '/cupid/profile/:id',
        name: 'CupidDetails',
        component: CupidDetails,
    },
    {
        path: '/cupid/gig/completed/:id',
        name: 'GigComplete',
        component: GigComplete,
    },
    {
        path: '/cupid/feedback/:id',
        name: 'CupidFeedback',
        component: CupidFeedback
    },
    {
        path: '/manager/home/:id',
        name: 'ManagerHome',
        component: ManagerHome,
    },
    {
        path: '/manager/cupids/:id',
        name: 'ManageCupids',
        component: Cupid
    },
    {
        path: '/manager/daters/:id',
        name: 'ManageDaters',
        component: Daters,
    },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// More lenient authentication guards
router.beforeEach(async (to, from, next) => {
    // Skip guards for login/public pages or non-protected routes
    if (to.name === 'Login' || to.name === 'Register' || !to.params.id) {
        next()
        return
    }

    // Extract user info from route
    const routeUserId = String(to.params.id)
    const routePath = to.path

    // Determine route type (dater, cupid, manager)
    let routeType = null
    if (routePath.includes('/dater/')) routeType = 'dater'
    else if (routePath.includes('/cupid/')) routeType = 'cupid'
    else if (routePath.includes('/manager/')) routeType = 'manager'

    // If no route type detected, allow navigation (might be a public route)
    if (!routeType) {
        next()
        return
    }

    // Validate against server-side session instead of trusting URL/localStorage
    try {
        const session = await makeRequest('/api/session/', 'get')
        const serverUserId = String(session.id)
        const serverUserRole = session.role

        // If server reports a different role, redirect them to their own home
        if (serverUserRole !== routeType) {
            redirectToCorrectHome(serverUserRole, serverUserId)
            return
        }

        // If the roles match but the IDs differ, deny navigation unless the user
        // is a manager (managers are allowed to view management pages for others)
        if (serverUserRole !== 'manager' && serverUserId !== routeUserId) {
            redirectToCorrectHome(serverUserRole, serverUserId)
            return
        }

        // All good
        next()
    } catch (err) {
        // Server session missing or request failed — treat as unauthenticated
        console.warn('Server session not available; redirecting to Login', err)
        next({ name: 'Login' })
    }
})

// Helper function to redirect to correct home
function redirectToCorrectHome(userType, userId) {
  const homeRoutes = {
    'dater': { name: 'DaterHome', params: { id: userId } },
    'cupid': { name: 'CupidHome', params: { id: userId } },
    'manager': { name: 'ManagerHome', params: { id: userId } }
  }
  
  const correctRoute = homeRoutes[userType]
  if (correctRoute) {
    router.push(correctRoute)
  }
}

export default router
