using System;
using System.IO;
using OpenCvSharp;
using OpenCvSharp.XFeatures2D;

namespace CV
{
    class Program
    {
        public Program()
        {

        }
        static void Main(string[] args)
        {
            Program pr = new Program();
            pr.MultiMatch(".\\GD.png", ".\\STAR.png");

            //Mat Map = new Mat(".\\GZ.png");
            //Cv2.ImShow("Matches", pr.MapTransf(Map));
            //Cv2.WaitKey();

        }
        Mat MapTransf(Mat Map)
        {
            Mat Background = new Mat(Map.Size(), MatType.CV_8UC3, new Scalar(255, 255, 255));
            Mat After = new Mat();
            Map = Map.CvtColor(ColorConversionCodes.RGB2HSV);
            Scalar lowerb = new Scalar(104, 180, 46);
            Scalar upperb = new Scalar(105, 255, 255);
            Mat Mask = Map.InRange(lowerb, upperb);

            Map.CopyTo(Map, Mask);
            Background.CopyTo(Mask, Mask);
            Cv2.Subtract(Background, Mask, Background);

            Cv2.AddWeighted(Map, 1, Background, 1, 0, After);
            return After;
        }
        void MultiMatch(string reference, string template)
        {
            Mat Input = new Mat(reference);
            Mat After = MapTransf(Input);
            After.Add(Input);
            using (Mat refMat = After)
            //using (Mat refMat = new Mat(reference))
            using (Mat tplMat = new Mat(template))
            using (Mat res = new Mat(refMat.Rows - tplMat.Rows + 1, refMat.Cols - tplMat.Cols + 1, MatType.CV_32FC1))
            {

                //Convert input images to gray
                Mat gref = refMat.CvtColor(ColorConversionCodes.BGR2GRAY);
                Mat gtpl = tplMat.CvtColor(ColorConversionCodes.BGR2GRAY);

                Cv2.MatchTemplate(gref, gtpl, res, TemplateMatchModes.CCoeffNormed);
                Cv2.Threshold(res, res, 0.8, 1.0, ThresholdTypes.Tozero);
                FileStream fs = new FileStream("D:\\XY.txt", FileMode.CreateNew);
                StreamWriter sw = new StreamWriter(fs);
                while (true)
                {
                    double minval, maxval, threshold = 0.8;
                    Point minloc, maxloc;
                    Cv2.MinMaxLoc(res, out minval, out maxval, out minloc, out maxloc);
                    if (maxval >= threshold)
                    {
                        //Setup the rectangle to draw
                        Rect r = new Rect(new Point(maxloc.X, maxloc.Y), new Size(tplMat.Width, tplMat.Height));
                        Console.WriteLine($"MinVal={minval.ToString()} MaxVal={maxval.ToString()} MinLoc={minloc.ToString()} MaxLoc={maxloc.ToString()} Rect={r.ToString()}");
                        sw.WriteLine(r.X + "#*#" + r.Y);
                        //Draw a rectangle of the matching area
                        Cv2.Rectangle(refMat, r, Scalar.LimeGreen, 2);

                        //Fill in the res Mat so you don't find the same area again in the MinMaxLoc
                        Rect outRect;
                        Cv2.FloodFill(res, maxloc, new Scalar(0), out outRect, new Scalar(0.1), new Scalar(1.0), FloodFillFlags.Link4);
                    }
                    else
                        break;
                }
                sw.Close();
                fs.Close();
                Cv2.ImShow("Matches", refMat);
                Cv2.WaitKey();
            }

        }
        void GetMatch(Mat src1,Mat src2)
        {

            Mat src3 = new Mat();
            Mat src4 = new Mat();
            Mat element = Cv2.GetStructuringElement(MorphShapes.Rect, new Size(50, 50));
            //Cv2.Erode(src1, src3, element);
            //Cv2.Dilate(src3, src3, element);
            //Cv2.Erode(src2, src4, element);
            //Cv2.Dilate(src4, src4, element);

            SIFT sift = SIFT.Create();
            SURF surf = SURF.Create(5000);
            KeyPoint[] keypoints1;
            KeyPoint[] keypoints2;
            MatOfFloat descriptors1 = new MatOfFloat();
            MatOfFloat descriptors2 = new MatOfFloat();
            surf.DetectAndCompute(src1, null, out keypoints1, descriptors1);
            surf.DetectAndCompute(src2, null, out keypoints2, descriptors2);

            // Matching descriptor vectors with a brute force matcher
            BFMatcher matcher1 = new BFMatcher(NormTypes.L1,true);
            //BFMatcher matcher2 = new BFMatcher(NormTypes.L2, true);
            //BFMatcher matcher3 = new BFMatcher(NormTypes.L2SQR, true);

            //FlannBasedMatcher matcher4 = new FlannBasedMatcher();
            DMatch[] matches1 = matcher1.Match(descriptors1, descriptors2);
            //DMatch[] matches2 = matcher2.Match(descriptors1, descriptors2);
            //DMatch[] matches3 = matcher3.Match(descriptors1, descriptors2);
            //int score = matches3.Length + matches2.Length + matches3.Length;
            Console.WriteLine("X:" + keypoints2[0].Pt.X.ToString() + " Y:" + keypoints2[0].Pt.Y.ToString());

            //Console.WriteLine("Score:" + score);
            //Console.WriteLine("Total:" + Temp);
            //Console.WriteLine("Times:" + Times);

            // Draw matches
            Mat view1 = new Mat();
            //Mat view2 = new Mat();
            //Mat view3 = new Mat();

            Cv2.DrawMatches(src1, keypoints1, src2, keypoints2, matches1, view1);
            //Cv2.DrawMatches(src1, keypoints1, src2, keypoints2, matches2, view2);
            //Cv2.DrawMatches(src1, keypoints1, src2, keypoints2, matches3, view3);


            for (int i = 0; i < keypoints1.Length; i++)
            {
                Console.WriteLine("X:" + keypoints1[i].Pt.X.ToString() + " Y:" + keypoints1[i].Pt.Y.ToString());
                Console.WriteLine("");
            }
            using (new Window("NORM_L1", WindowMode.AutoSize, view1))
            //using (new Window("NORM_L2", WindowMode.AutoSize, view2))
            //using (new Window("NORM_L2SQR", WindowMode.AutoSize, view3))
            //if (score >= 150)
            {
                //    Cv2.Resize(src2, src2, new Size(512, 389));
                //    using (new Window("Slide", WindowMode.AutoSize, src2))
                //    {

                Cv2.WaitKey();
                //    }
            }
        }
        void GetHisto(Mat src)
        {
            // Histogram view
            const int Width = 640, Height = 512;
            Mat render = new Mat(new Size(Width, Height), MatType.CV_8UC3, Scalar.All(255));

            // Calculate histogram
            Mat hist = new Mat();
            int[] hdims = { 256 }; // Histogram size for each dimension
            Rangef[] ranges = { new Rangef(0, 256), }; // min/max 
            Cv2.CalcHist(
                new Mat[] { src },
                new int[] { 0 },
                null,
                hist,
                1,
                hdims,
                ranges);

            // Get the max value of histogram
            double minVal, maxVal;
            Cv2.MinMaxLoc(hist, out minVal, out maxVal);

            Scalar color = Scalar.All(100);
            // Scales and draws histogram
            hist = hist * (maxVal != 0 ? Height / maxVal : 0.0);
            for (int j = 0; j < hdims[0]; ++j)
            {
                int binW = (int)((double)Width / hdims[0]);
                render.Rectangle(
                    new Point(j * binW, render.Rows - (int)(hist.Get<float>(j))),
                    new Point((j + 1) * binW, render.Rows),
                    color,
                    -1);
            }

            using (new Window("Image", WindowMode.AutoSize | WindowMode.FreeRatio, src))
            using (new Window("Histogram", WindowMode.AutoSize | WindowMode.FreeRatio, render))
            {
                Cv2.WaitKey();
            }
        }

        void GetEdge(Mat src)
        {
            Mat dst1 = new Mat();
            Mat dst2 = new Mat();
            Cv2.Canny(src, dst1, 50, 500);
            Cv2.Canny(src, dst2, 250, 500);
            using (new Window("GetEdge1", dst1))
            using (new Window("GetEdge2", dst2))
            {
                Cv2.WaitKey();
            }
        }

        void GetPixel(Mat src)
        {
            Mat dst1 = new Mat();
            Mat dst2 = new Mat();
            src.CopyTo(dst1);
            src.CopyTo(dst2);
            for (int y = 0; y < src.Height; y++)
            {
                for (int x = 0; x < src.Width; x++)
                {
                    Vec3b color = src.Get<Vec3b>(y, x);

                    Vec3b color1 = new Vec3b();
                    color1.Item0 = color.Item1; // R <- G
                    color1.Item1 = color.Item2; // G <- B
                    Vec3b color2 = new Vec3b();
                    color2.Item2 = color.Item1; // B <- G
                    color2.Item1 = color.Item0; // G <- R

                    dst1.Set<Vec3b>(y, x, color1);
                    dst2.Set<Vec3b>(y, x, color2);
                }
            }
            using (new Window("GetPixel1", dst1))
            using (new Window("GetPixel2", dst2))
            {
                Cv2.WaitKey();
            }
        }
    }
}
