ob = opticalFlowLK;
im1 =  imread('frame10.png');
im2 =  imread('frame11.png');

inp = {im1, im2};
a = inp{1};
n = 1;
while n <= 2
    frameGray = rgb2gray(inp{n});

    flow = estimateFlow(ob,frameGray);

    imshow(im1)
    hold on
    plot(flow,'DecimationFactor',[5 5],'ScaleFactor',10)
    hold off
    n = n+1;
end