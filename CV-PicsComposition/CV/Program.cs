using System;
using System.Collections;
using System.Collections.Generic;
using System.Numerics;
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
            Mat target = new Mat(".\\target.jpg", ImreadModes.Color);
            Mat background = new Mat(".\\background.jpg", ImreadModes.Color);
            Mat result = new Mat(background.Size(), background.Type());
            Cv2.MatchTemplate(background, target, result, TemplateMatchModes.SqDiff);
            Point minPoint;
            Point maxPoint;
            double minVal = 0;
            double maxVal = 0;
            Cv2.MinMaxLoc(result, out minVal, out maxVal, out minPoint, out maxPoint);
            Cv2.Rectangle(background, minPoint, new Point(minPoint.X + target.Cols, minPoint.Y + target.Rows), new Scalar(255, 0, 0), 5, LineTypes.Link8);
            

            using (new Window("背景", WindowMode.FreeRatio, background))
            using (new Window("模板", WindowMode.FreeRatio, target))
            {
                Cv2.WaitKey();
            }

        }


    }
}
