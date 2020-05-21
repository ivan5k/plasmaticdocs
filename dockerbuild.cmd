# First instlal Docker for Windows

docker pull keimlink/sphinx-doc

docker run -it --rm -v "D:\Ivan\Plasmatron\docs":/home/python/docs keimlink/sphinx-doc:1.7.1 make -C docs html

pause