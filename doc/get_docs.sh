urls=(http://yann.lecun.com/exdb/publis/pdf/lecun-dave-05.pdf yann.lecun.com/exdb/publis/pdf/sermanet-jfr-09.pdf http://ceit.aut.ac.ir/~shiry/publications/AI03.pdf)

echo "get_docs.sh > Starting Download"
for url in ${urls[@]}
do
	wget -c $url 
done
echo "get_docs.sh > Download Complete"
