//
//  BMEPointGraphView.m
//  BeMyEyes
//
//  Created by Simon Støvring on 04/04/14.
//  Copyright (c) 2014 Be My Eyes. All rights reserved.
//

#import "BMEPointGraphView.h"
#import "BMEPointGraphEntry.h"

#define BMEPointGraphDefaultStrokeWidth 4.0f
#define BMEPointGraphDefaultStrokeColor [UIColor blackColor]
#define BMEPointGraphDefaultGradientStartColor [UIColor whiteColor]
#define BMEPointGraphDefaultGradientEndColor [UIColor blueColor]
#define BMEPointGraphDefaultGraphInsets UIEdgeInsetsMake(30.0f, -2.0f, 30.0f, 30.0f);

@interface BMEPointGraphView ()
@property (weak, nonatomic) IBOutlet UIImageView *starImageView;

@property (weak, nonatomic) IBOutlet NSLayoutConstraint *starCenterXMarginConstraint;
@property (weak, nonatomic) IBOutlet NSLayoutConstraint *starCenterYMarginConstraint;

@property (strong, nonatomic) NSMutableArray *entries;
@property (assign, nonatomic) CGFloat pixelsPerSecond;
@property (assign, nonatomic) CGFloat pixelsPerPoint;
@property (assign, nonatomic) CGSize adjustedSize;

@property (strong, nonatomic) CAEmitterLayer *emitterLayer;
@end

@implementation BMEPointGraphView

#pragma mark -
#pragma mark Lifecycle

- (id)init {
    if (self = [super init]) {
        [self initialize];
    }
    
    return self;
}

- (id)initWithFrame:(CGRect)frame {
    if (self = [super initWithFrame:frame]) {
        [self initialize];
    }
    
    return self;
}

- (id)initWithCoder:(NSCoder *)aDecoder {
    if (self = [super initWithCoder:aDecoder]) {
        [self initialize];
    }
    
    return self;
}

- (void)initialize {
    self.starImageView.hidden = YES;
    
    self.strokeWidth = BMEPointGraphDefaultStrokeWidth;
    self.strokeColor = BMEPointGraphDefaultStrokeColor;
    self.gradientStartColor = BMEPointGraphDefaultGradientStartColor;
    self.gradientEndColor = BMEPointGraphDefaultGradientEndColor;
    self.calculatesMinimum = YES;
    self.calculatesMaximum = YES;
    self.graphInsets = BMEPointGraphDefaultGraphInsets;
}

- (void)drawRect:(CGRect)rect {
    [self clearDrawing];

    if (self.emitterLayer) {
        [self.emitterLayer removeFromSuperlayer];
    }
    
    if ([self.entries count] > 0) {
        [self drawGraph];
        [self placeStar];
        [self placeParticleEmitter];
    }
}

- (void)dealloc {
    self.entries = nil;
    self.emitterLayer = nil;
}

#pragma mark -
#pragma mark Public Methods

- (void)addPoints:(NSUInteger)points atDate:(NSDate *)date {
    BMEPointGraphEntry *entry = [BMEPointGraphEntry entryWithPoints:points date:date];
    [self.entries addObject:entry];
}

- (void)draw {
    if ([self.entries count] > 0) {
        NSSortDescriptor *dateSortDescriptor = [NSSortDescriptor sortDescriptorWithKey:@"date" ascending:YES];
        [self.entries sortUsingDescriptors:@[ dateSortDescriptor ]];
        
        if (self.calculatesMaximum) {
            self.minimum = [[self.entries valueForKeyPath:@"@min.points"] unsignedIntegerValue];
        }
        
        if (self.calculatesMaximum) {
            self.maximum = [[self.entries valueForKeyPath:@"@max.points"] unsignedIntegerValue];
        }
        
        self.adjustedSize = CGSizeMake(CGRectGetWidth(self.bounds) - self.graphInsets.left - self.graphInsets.right,
                                       CGRectGetHeight(self.bounds) - self.graphInsets.top - self.graphInsets.bottom);
        
        NSTimeInterval timeDifference = [[self lastEntry].date timeIntervalSinceDate:[self firstEntry].date];
        self.pixelsPerSecond = self.adjustedSize.width / timeDifference;
        self.pixelsPerPoint = self.adjustedSize.height / (self.maximum - self.minimum);
    }
    
    [self setNeedsDisplay];
}

#pragma mark -
#pragma mark Private Methods

- (void)placeStar {
    CGPoint lastPoint = CGPointMake([self xForDate:[self lastEntry].date], [self yForPoints:[self lastEntry].points]);
    CGPoint starCenter = CGPointZero;
    starCenter.x = CGRectGetMidX(self.bounds) - lastPoint.x;
    starCenter.y = CGRectGetMidY(self.bounds) - lastPoint.y;
    
    self.starCenterXMarginConstraint.constant = starCenter.x;
    self.starCenterYMarginConstraint.constant = starCenter.y;
    [self layoutIfNeeded];
    
    self.starImageView.hidden = NO;
}

- (void)placeParticleEmitter {
    CAEmitterCell *emitterCell = [CAEmitterCell emitterCell];
    emitterCell.contents = (id)[[UIImage imageNamed:@"PointGraphStar"] CGImage];
    emitterCell.birthRate = 0.0f;
    emitterCell.lifetime = 1.0f;
    emitterCell.lifetimeRange = 0.15f;
    emitterCell.velocity = 80.0f;
    emitterCell.emissionRange = 2.0f * M_PI;
    emitterCell.spin = 0.20f;
    emitterCell.spinRange = 2.0f;
    emitterCell.scale = 0.30f;
    emitterCell.scaleRange = 0.10f;
    emitterCell.alphaRange = 0.0f;
    emitterCell.alphaSpeed = -1.0f;
    emitterCell.birthRate = 3.0f;
    
    self.emitterLayer = [CAEmitterLayer layer];
    self.emitterLayer.bounds = CGRectMake(0.0f, 0.0f, CGRectGetWidth(self.bounds), CGRectGetHeight(self.bounds));
    self.emitterLayer.position = CGPointMake(CGRectGetMidX(self.bounds), CGRectGetMidY(self.bounds));
    self.emitterLayer.backgroundColor = [[UIColor clearColor] CGColor];
    self.emitterLayer.emitterPosition = self.starImageView.center;
    self.emitterLayer.emitterSize = self.starImageView.frame.size;
    self.emitterLayer.emitterCells = @[ emitterCell ];
    [self.layer addSublayer:self.emitterLayer];
}

- (void)drawGraph {
    CGContextSetStrokeColorWithColor(UIGraphicsGetCurrentContext(), [self.strokeColor CGColor]);
    
    CGMutablePathRef linePath = CGPathCreateMutable();
    CGMutablePathRef fillPath = CGPathCreateMutable();
    
    CGPoint firstFillPoint = CGPointMake([self xForDate:[self firstEntry].date] - self.strokeWidth * 0.50f, [self yForPoints:self.minimum] + self.graphInsets.bottom);
    CGPathMoveToPoint(fillPath, NULL, firstFillPoint.x, firstFillPoint.y);
    
    CGPoint firstEntryFillPoint = CGPointMake([self xForDate:[self firstEntry].date] - self.strokeWidth * 0.50f, [self yForPoints:[self firstEntry].points]);
    CGPathAddLineToPoint(fillPath, NULL, firstEntryFillPoint.x, firstEntryFillPoint.y);
    
    CGPoint firstPoint = CGPointMake([self xForDate:[self firstEntry].date], [self yForPoints:[self firstEntry].points]);
    CGPathMoveToPoint(linePath, NULL, firstPoint.x, firstPoint.y);
    CGPathAddLineToPoint(fillPath, NULL, firstPoint.x, firstPoint.y);
    
    NSInteger entriesCount = [self.entries count];
    
    for (NSInteger i = 1; i < entriesCount; i++) {
        BMEPointGraphEntry *entry = self.entries[i];
        CGPoint point = CGPointMake([self xForDate:entry.date], [self yForPoints:entry.points]);
        CGPathAddLineToPoint(linePath, NULL, point.x, point.y);
        CGPathAddLineToPoint(fillPath, NULL, point.x, point.y);
    }
    
    CGPoint lastEntryFillPoint = CGPointMake([self xForDate:[self lastEntry].date] + self.strokeWidth * 0.50f, [self yForPoints:[self lastEntry].points]);
    CGPathAddLineToPoint(fillPath, NULL, lastEntryFillPoint.x, lastEntryFillPoint.y);
    
    CGPoint lastFillPoint = CGPointMake([self xForDate:[self lastEntry].date] + self.strokeWidth * 0.50f, [self yForPoints:self.minimum] + self.graphInsets.bottom);
    CGPathAddLineToPoint(fillPath, NULL, lastFillPoint.x, lastFillPoint.y);
    
    [self drawGradientInPath:fillPath];
    
    UIBezierPath *lineBezier = [UIBezierPath bezierPathWithCGPath:linePath];
    lineBezier.lineJoinStyle = kCGLineJoinRound;
    lineBezier.lineWidth = self.strokeWidth;
    [lineBezier stroke];
    
    CGPathRelease(linePath);
    CGPathRelease(fillPath);
}

- (void)drawGradientInPath:(CGPathRef)path {
    if (path) {
        CGContextSaveGState(UIGraphicsGetCurrentContext());
        CGContextAddPath(UIGraphicsGetCurrentContext(), path);
        CGContextClip(UIGraphicsGetCurrentContext());
    }
    
    NSArray *gradientColors = @[ (id)[self.gradientStartColor CGColor], (id)[self.gradientEndColor CGColor] ];
    CGFloat gradientLocations[2];
    gradientLocations[0] = 0.0f;
    gradientLocations[1] = 1.0f;
    
    CGColorSpaceRef rgbSpace = CGColorSpaceCreateDeviceRGB();
    CGGradientRef gradient = CGGradientCreateWithColors(rgbSpace, (__bridge CFArrayRef)gradientColors, gradientLocations);
    CGColorSpaceRelease(rgbSpace);
    
    CGPoint gradientStart = CGPointZero;
    CGPoint gradientEnd = CGPointMake(0.0f, self.adjustedSize.height - [self yForPoints:self.maximum]);
    CGContextDrawLinearGradient(UIGraphicsGetCurrentContext(), gradient, gradientStart, gradientEnd, kCGGradientDrawsBeforeStartLocation | kCGGradientDrawsAfterEndLocation);
    
    if (path) {
        CGContextRestoreGState(UIGraphicsGetCurrentContext());
    }
}

- (void)clearDrawing {
    CGContextClearRect(UIGraphicsGetCurrentContext(), self.bounds);
    CGContextSetFillColorWithColor(UIGraphicsGetCurrentContext(), [self.backgroundColor CGColor]);
    CGContextFillRect(UIGraphicsGetCurrentContext(), self.bounds);
}

- (CGFloat)xForDate:(NSDate *)date {
    return [date timeIntervalSinceDate:[self firstEntry].date] * self.pixelsPerSecond + self.graphInsets.left;
}

- (CGFloat)yForPoints:(NSUInteger)points {
	return self.adjustedSize.height - ((points - self.minimum) * self.pixelsPerPoint) + self.graphInsets.top;
}

- (BMEPointGraphEntry *)firstEntry {
    return [self.entries firstObject];
}

- (BMEPointGraphEntry *)lastEntry {
    return [self.entries lastObject];
}

- (NSMutableArray *)entries {
    if (!_entries) {
        _entries = [NSMutableArray new];
    }
    
    return _entries;
}

@end


