hexo.extend.filter.register('theme_inject', function(injects) {
  injects.bodyBegin.raw('default', '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7406269002228687"\n' +
      '     crossorigin="anonymous"></script>');
});