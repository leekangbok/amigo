import lazyloading from './lazyLoading'

export default [{
    text: '고객관리',
    path: '/customer',
    icon: 'people',
    pri: 201,
    component: lazyloading('customer', true)
  },
  {
    path: '/customer/add',
    component: lazyloading('customer/CustomerAdd')
  }
]
