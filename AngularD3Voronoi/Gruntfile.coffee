module.exports = (grunt) ->
  # configuration
  grunt.initConfig
   
    coffee:
      compile:
        expand: true
        cwd: 'src'
        src: ['**/*.coffee']
        dest: 'dist/js'
        ext: '.js'
        options:
          bare: true
          preserve_dirs: true

  # load plugins
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  
  # tasks
  grunt.registerTask 'default', ['coffee']