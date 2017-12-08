import lazyloading from './lazyLoading'

const bitcoin = {
  text: '축구',
  path: '/blog/bitcoin',
  icon: 'attach_money',
  component: lazyloading('blog/bitcoin')
}

const python = {
  text: '농구',
  path: '/blog/python',
  icon: 'attach_money',
  component: lazyloading('blog/python')
}

export default [{
  text: '블로그',
  icon: 'rss_feed',
  pri: 100,
  model: false,
  children: [bitcoin, python]
}]
