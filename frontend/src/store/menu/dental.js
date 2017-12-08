import lazyloading from './lazyLoading'

const dashBoard = {
  text: '대시보드',
  path: '/dental/DashBoard',
  component: lazyloading('dental/DashBoard')
}

const intro = {
  text: 'Intro',
  path: '/dental/Intro',
  component: lazyloading('dental/Intro'),
  children: [{
      path: 'default',
      component: lazyloading('dental/IntroDefault')
    },
    {
      path: 'Profile',
      component: lazyloading('dental/Profile')
    },
    {
      path: 'Home',
      component: lazyloading('dental/Home')
    },
    {
      path: 'Consulting',
      name: 'DentalConsulting',
      component: lazyloading('dental/Consulting'),
      props: true
    },
    {
      path: 'Reservation',
      component: lazyloading('dental/Reservation')
    },
    {
      path: 'ConsultingAdd',
      component: lazyloading('dental/ConsultingAdd')
    },
    {
      path: 'ConsultingEdit',
      name: 'DentalConsultingEdit',
      component: lazyloading('dental/ConsultingEdit'),
      props: true
    }
  ]
}

const takeOver = {
  text: '접수',
  path: '/dental/TakeOver',
  component: lazyloading('dental/TakeOver')
}

export default [{
    text: '오치과',
    icon: 'fullscreen_exit',
    pri: 70,
    model: true,
    children: [intro, takeOver, dashBoard]
  },
  {
    path: '/dental/UserAdd',
    component: lazyloading('dental/UserAdd')
  }
]
