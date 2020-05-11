function p=softmax(a,link,bias)
for i=1:3
    z(i)=dot(a(2,:),link(3,i,:))+bias(3,i);
end
output=exp(z);
ot=0;
for i=1:3
    ot=ot+output(i);
    if i==3
        p(i)=output(i)/ot;
        p(i-1)=output(i-1)/ot;
        p(i-2)=output(i-2)/ot;
    end
end
